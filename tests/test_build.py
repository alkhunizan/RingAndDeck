import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import sys
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "profile_builder", Path(__file__).parents[1] / "scripts/build.py"
)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def catalog():
    return {
        "id": "example",
        "name": "Example Workflow",
        "version": "0.1.0",
        "description": "A portable prompt deck.",
        "prompts": {
            "check": {
                "title": "Check the evidence",
                "text": "Verify the supplied evidence.",
            }
        },
        "pages": [
            {
                "id": "home",
                "title": "Home",
                "color": "#0e7490",
                "symbol": "code",
                "buttons": [
                    {
                        "slot": "0,0",
                        "kind": "folder",
                        "page": "review",
                        "label": ["REVIEW"],
                    },
                    {
                        "slot": "1,0",
                        "kind": "prompt",
                        "prompt": "check",
                        "label": ["CHECK"],
                    },
                ],
            },
            {
                "id": "review",
                "title": "Review",
                "color": "#0e7490",
                "symbol": "check",
                "buttons": [
                    {
                        "slot": "1,0",
                        "kind": "prompt",
                        "prompt": "check",
                        "label": ["CHECK"],
                    },
                ],
            },
        ],
    }


class ProfileBuildTests(unittest.TestCase):
    def test_public_browser_links_and_allowlisted_shortcuts(self):
        data = catalog()
        data["pages"][0]["buttons"] += [
            {
                "slot": "2,0",
                "kind": "website",
                "url": "https://github.com/",
                "label": ["GITHUB"],
            },
            {
                "slot": "3,0",
                "kind": "hotkey",
                "shortcut": "reopen-tab",
                "label": ["REOPEN", "TAB"],
            },
        ]
        files = builder.build_profile(data)
        actions = [
            a
            for name, raw in files.items()
            if name.endswith("manifest.json") and "/Profiles/" in name
            for c in json.loads(raw)["Controllers"]
            for a in c["Actions"].values()
        ]
        self.assertEqual(
            next(a for a in actions if a["UUID"].endswith(".website"))["Settings"][
                "path"
            ],
            "https://github.com/",
        )
        self.assertEqual(
            next(a for a in actions if a["UUID"].endswith(".hotkey"))["Settings"][
                "Hotkeys"
            ][0]["VKeyCode"],
            84,
        )
        for url in [
            "file:///private",
            "https://user:pass@example.org/",
            "https://example.org/?account=123",
            "https://127.0.0.1/",
            "https://[::1]/",
            "https://169.254.169.254/",
            "https://2130706433/",
            "https://0x7f000001/",
            "https://printer.local/",
            "https://private.lan/",
        ]:
            data["pages"][0]["buttons"][2]["url"] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                builder.validate_catalog(data)

    def test_removed_or_renamed_outputs_cannot_silently_survive_a_rebuild(self):
        parent = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(prefix="deck-test-", dir=parent) as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(parent))
            (root / "profiles").mkdir()
            source = root / "profiles/example.json"
            data = catalog()
            source.write_text(json.dumps(data), encoding="utf-8")
            builder.compile_repository(root)
            data["version"] = "0.2.0"
            source.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Stale generated"):
                builder.compile_repository(root)
            with self.assertRaisesRegex(ValueError, "Stale generated"):
                builder.compile_repository(root, check=True)

    def test_inventory_tracks_removed_guides_and_rejects_unsafe_entries(self):
        parent = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(prefix="deck-test-", dir=parent) as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(parent))
            (root / "profiles").mkdir()
            source = root / "profiles/example.json"
            data = catalog()
            source.write_text(json.dumps(data), encoding="utf-8")
            builder.compile_repository(root)
            builder.compile_repository(root, check=True)
            inventory = root / ".generated-files.json"
            self.assertIn("docs/example.md", json.loads(inventory.read_text()))
            data["id"] = "renamed"
            source.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Stale generated.*docs/example.md"):
                builder.compile_repository(root)
            inventory.write_text(json.dumps(["../outside.md"]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid generated-file inventory"):
                builder.compile_repository(root)

    def test_empty_repository_and_duplicate_catalog_ids_are_rejected(self):
        parent = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(prefix="deck-test-", dir=parent) as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(parent))
            (root / "profiles").mkdir()
            with self.assertRaisesRegex(ValueError, "At least one"):
                builder.compile_repository(root)
            for filename in ("first.json", "second.json"):
                (root / "profiles" / filename).write_text(
                    json.dumps(catalog()), encoding="utf-8"
                )
            with self.assertRaisesRegex(ValueError, "Catalog ids must be unique"):
                builder.compile_repository(root)

    def test_import_package_has_real_default_page_and_resolvable_folders(self):
        files = builder.build_profile(catalog())
        self.assertTrue(files, "Builder must emit an importable profile")
        roots = {name.split("/")[0] for name in files}
        self.assertEqual(len(roots), 1)
        root = roots.pop()
        self.assertTrue(root.endswith(".sdProfile"))
        top = json.loads(files[f"{root}/manifest.json"])
        self.assertEqual(top["Pages"]["Default"], top["Pages"]["Current"])
        self.assertIn(top["Pages"]["Default"], top["Pages"]["Pages"])
        self.assertEqual(top["AppIdentifier"], "")
        self.assertNotIn("UUID", top["Device"])
        home = json.loads(
            files[f"{root}/Profiles/{top['Pages']['Default']}/manifest.json"]
        )
        actions = home["Controllers"][0]["Actions"]
        folder = actions["0,0"]["Settings"]["ProfileUUID"]
        child = json.loads(files[f"{root}/Profiles/{folder}/manifest.json"])
        self.assertEqual(
            child["Controllers"][0]["Actions"]["0,0"]["UUID"],
            "com.elgato.streamdeck.profile.backtoparent",
        )
        for filename, raw in files.items():
            if not filename.endswith("manifest.json") or "/Profiles/" not in filename:
                continue
            page = json.loads(raw)
            for action in page["Controllers"][0]["Actions"].values():
                state = action["States"][0]
                self.assertIn(
                    str(Path(filename).parent.as_posix()) + "/" + state["Image"], files
                )
                if action["UUID"].endswith(".text"):
                    self.assertFalse(action["Settings"]["isSendingEnter"])
                    self.assertFalse(action["Settings"]["isTypingMode"])
                    self.assertIn(
                        "Verify the supplied evidence.",
                        action["Settings"]["pastedText"],
                    )

    def test_archive_is_reproducible_and_contains_no_absolute_paths(self):
        files = builder.build_profile(catalog())
        a = builder.package_profile(files)
        self.assertEqual(a, builder.package_profile(builder.build_profile(catalog())))
        with zipfile.ZipFile(io.BytesIO(a)) as archive:
            self.assertIsNone(archive.testzip())
            self.assertTrue(archive.namelist())
            for name in archive.namelist():
                self.assertNotIn("..", name.split("/"))
                self.assertNotIn("\\", name)
                self.assertFalse(name.startswith("/"))

    def test_duplicate_slots_broken_folders_and_unsafe_actions_are_rejected(self):
        for mutation in (
            "duplicate",
            "broken",
            "unsafe",
            "back_slot",
            "label",
            "private",
            "version",
            "title_private",
            "orphan",
            "cycle",
        ):
            data = catalog()
            if mutation == "duplicate":
                data["pages"][0]["buttons"].append(
                    copy.deepcopy(data["pages"][0]["buttons"][0])
                )
            elif mutation == "broken":
                data["pages"][0]["buttons"][0]["page"] = "missing"
            elif mutation == "unsafe":
                data["pages"][0]["buttons"][1]["kind"] = "shell"
            elif mutation == "back_slot":
                data["pages"][1]["buttons"][0]["slot"] = "0,0"
            elif mutation == "label":
                data["pages"][0]["buttons"][0]["label"] = ["A label much too long"]
            elif mutation == "private":
                data["prompts"]["check"]["text"] = (
                    "Open " + "C:" + "\\Users\\example\\private.txt"
                )
            elif mutation == "version":
                data["version"] = "../../outside"
            elif mutation == "title_private":
                data["name"] = "person" + "@" + "example.org"
            elif mutation == "orphan":
                data["pages"][0]["buttons"].pop(0)
            else:
                data["pages"][1]["buttons"].append(
                    {
                        "slot": "2,0",
                        "kind": "folder",
                        "page": "review",
                        "label": ["LOOP"],
                    }
                )
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                builder.validate_catalog(data)

    def test_private_paths_contact_details_and_tokens_are_flagged(self):
        self.assertTrue(builder.privacy_findings("/local-only-action"))
        for text in [
            "C:" + "\\Users\\example\\work",
            "email " + "person" + "@" + "example.org",
            "token " + "ghp_" + "A" * 36,
            "http://127.0.0.1:8080/private",
            "https://example.org/?api_key=" + "x" * 25,
        ]:
            with self.subTest(text=text[:12]):
                self.assertTrue(builder.privacy_findings(text))
        self.assertEqual(
            builder.privacy_findings(
                "Use the approved workspace and ask before publishing."
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
