import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ring


def sample():
    return {
        "id": "sample-ring",
        "name": "Sample Ring",
        "version": "0.1.0",
        "description": "Example",
        "folders": [
            {
                "id": "focus",
                "title": "Focus",
                "color": "#7DCEC2",
                "icon": "timer",
                "actions": [
                    {
                        "id": "plan",
                        "title": "Plan",
                        "kind": "prompt",
                        "text": "Plan the supplied task.",
                    },
                    {
                        "id": "capture",
                        "title": "Capture",
                        "kind": "hotkey",
                        "shortcut": "capture",
                    },
                ],
            }
        ],
    }


class RingTests(unittest.TestCase):
    def test_home_folders_use_a_declared_application_mode(self):
        root = Path(__file__).resolve().parents[1]
        for catalog_id in ("code-ring", "work-ring", "flow-ring"):
            with self.subTest(catalog=catalog_id):
                catalog = json.loads(
                    (root / "rings" / f"{catalog_id}.json").read_text(encoding="utf-8")
                )
                files = ring.build_ring(catalog)
                profile = json.loads(files["ProfileInfo.json"])
                app = json.loads(files["ApplicationInfo.json"])
                declared_modes = {mode["name"] for mode in app["modes"]}
                self.assertEqual(declared_modes, {"System"})
                folder_actions = {
                    action["name"]
                    for action in profile["profileActions"]
                    if action["templateActionName"].endswith("OpenFolder")
                }
                self.assertTrue(folder_actions)
                modes = profile["layout"]["layoutModes"]
                self.assertTrue(modes)
                for mode in modes:
                    self.assertIn(mode["modeName"], declared_modes)
                    workspaces = {
                        workspace["name"]: workspace for workspace in mode["workspaces"]
                    }
                    self.assertIn(mode["homeWorkspaceName"], workspaces)
                    home = workspaces[mode["homeWorkspaceName"]]
                    self.assertEqual(len(home["pressPages"]), 1)
                    controls = home["pressPages"][0]["controls"]
                    self.assertEqual(len(controls), 8)
                    self.assertEqual(
                        {control["controlId"] for control in controls},
                        set(range(8)),
                    )
                    self.assertTrue(
                        {control["pressAction"] for control in controls}
                        <= folder_actions
                    )

    def test_native_slot_limits_keep_every_action_reachable(self):
        root = Path(__file__).resolve().parents[1]
        for catalog_id, action_count in {
            "code-ring": 81,
            "work-ring": 81,
            "flow-ring": 72,
        }.items():
            with self.subTest(catalog=catalog_id):
                catalog = json.loads(
                    (root / "rings" / f"{catalog_id}.json").read_text(encoding="utf-8")
                )
                files = ring.build_ring(catalog)
                profile = json.loads(files["ProfileInfo.json"])
                commands = {
                    action["name"]: action for action in profile["profileActions"]
                }
                leaves = {
                    "$@Generic___@Macro___" + macro["name"]
                    for macro in profile["macroCommands"]
                } | {
                    name
                    for name, action in commands.items()
                    if action["templateActionName"].endswith("KeyboardKey")
                }
                self.assertEqual(len(leaves), action_count)
                pages = {
                    page["name"]: page for page in profile["layout"]["folderPages"]
                }
                home = profile["layout"]["layoutModes"][0]["workspaces"][0][
                    "pressPages"
                ][0]
                visited = set()
                reached = set()

                def visit(page):
                    self.assertNotIn(
                        page["name"], visited, "Navigation contains a cycle"
                    )
                    visited.add(page["name"])
                    controls = page["controls"]
                    self.assertLessEqual(
                        len(controls), 8 if page["name"] == home["name"] else 9
                    )
                    self.assertTrue(controls)
                    self.assertEqual(
                        {control["controlId"] for control in controls},
                        set(range(len(controls))),
                    )
                    for control in controls:
                        ref = control["pressAction"]
                        if ref in leaves:
                            self.assertNotIn(ref, reached)
                            reached.add(ref)
                        else:
                            self.assertIn(ref, commands)
                            action = commands[ref]
                            self.assertTrue(
                                action["templateActionName"].endswith("OpenFolder")
                            )
                            target = action["actionParameters"]["parameters"][
                                "folderName"
                            ]
                            self.assertIn(target, pages)
                            visit(pages[target])

                visit(home)
                self.assertEqual(reached, leaves)
                self.assertEqual(visited, set(pages) | {home["name"]})
                preview = json.loads(files["metadata/ProfilePreview.json"])
                self.assertEqual(len(preview["buttonPages"]), 8)
                source_categories = {folder["title"] for folder in catalog["folders"]}
                category_pages = [
                    page
                    for page in pages.values()
                    if page["displayName"] in source_categories
                ]
                self.assertEqual(len(category_pages), len(source_categories))
                self.assertTrue(
                    all(len(page["controls"]) == 9 for page in category_pages)
                )
                overflow = [
                    page
                    for page in pages.values()
                    if page["displayName"] == "More workflows"
                ]
                self.assertEqual(len(overflow), 0 if catalog_id == "flow-ring" else 1)
                if overflow:
                    self.assertEqual(len(overflow[0]["controls"]), 2)
                    self.assertEqual(
                        preview["buttonPages"][-1]["displayName"], "More workflows"
                    )

    def test_all_controls_images_and_text_commands_resolve(self):
        files = ring.build_ring(sample())
        profile = json.loads(files["ProfileInfo.json"])
        app = json.loads(files["ApplicationInfo.json"])
        self.assertEqual(profile["name"], app["defaultProfileName"])
        self.assertEqual(profile["applicationName"], "@_defaultwin")
        self.assertIsNone(app["processOrBundleName"])
        self.assertEqual(len(profile["macroCommands"]), 1)
        macro = profile["macroCommands"][0]
        self.assertEqual(macro["supportedOs"], "Win")
        self.assertEqual(len(macro["actions"]), 2)
        self.assertEqual(macro["actions"][0], "$@Generic___@Sleep___1000")
        self.assertEqual(macro["actions"][1], macro["actionEditorCommands"][0]["name"])
        self.assertEqual(
            macro["actionEditorCommands"][0]["templateName"], "$@Generic___@SendText"
        )
        self.assertEqual(
            macro["actionEditorCommands"][0]["actionParameters"]["useClipboard"], "true"
        )
        self.assertIn("Plan the supplied task.", macro["description"])
        known = {a["name"] for a in profile["profileActions"]} | {
            "$@Generic___@Macro___" + macro["name"]
        }
        layout = profile["layout"]
        workspace = layout["layoutModes"][0]["workspaces"][0]
        controls = (
            workspace["pressPages"][0]["controls"]
            + layout["folderPages"][0]["controls"]
        )
        for control in controls:
            ref = control["pressAction"]
            self.assertIn(ref, known)
            self.assertIn("ActionImages/" + ref + ".png", files)
            self.assertIn("ActionIcons/" + ref + ".ict", files)
        folder = next(
            a
            for a in profile["profileActions"]
            if a["templateActionName"].endswith("OpenFolder")
        )
        self.assertEqual(
            folder["actionParameters"]["parameters"]["folderName"],
            layout["folderPages"][0]["name"],
        )
        for name, data in files.items():
            if name.endswith(".png"):
                self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_private_content_broken_slots_and_unknown_commands_rejected(self):
        for mutation in [
            "personal",
            "duplicate",
            "overflow",
            "shortcut",
            "kind",
            "no-folders",
        ]:
            data = copy.deepcopy(sample())
            if mutation == "personal":
                data["folders"][0]["actions"][0]["text"] = (
                    "person" + "@" + "example.org"
                )
            elif mutation == "duplicate":
                data["folders"][0]["actions"][1]["id"] = "plan"
            elif mutation == "overflow":
                data["folders"][0]["actions"] *= 5
            elif mutation == "shortcut":
                data["folders"][0]["actions"][1]["shortcut"] = "run-anything"
            elif mutation == "kind":
                data["folders"][0]["actions"][0]["kind"] = "shell"
            else:
                data["folders"] = []
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                ring.validate_ring(data)


if __name__ == "__main__":
    unittest.main()
