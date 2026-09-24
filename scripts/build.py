"""Compile portable Actions Ring and Stream Deck profiles with shared artwork."""

import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import re
import uuid
import zipfile
from urllib.parse import urlparse

import artwork

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = uuid.UUID("a8ea7337-c0bd-43e5-b85b-52ed45e5371a")
BROWSER_KEYS = {
    "tab-search": (65, True),
    "reopen-tab": (84, True),
    "zoom-reset": (48, False),
}
GUARD = (
    "Work only within the scope and permissions I explicitly give in this chat. "
    "If a tool or source is unavailable, say so and provide a usable draft or manual steps. "
    "Never expose secrets. Ask before sending, publishing, deleting data, spending money, "
    "or rewriting shared history.\n\n"
)
PATTERNS = {
    "absolute Windows path": r"(?i)\b[a-z]:[\\/]",
    "home or network path": r"(?i)(?:/Users/|/home/|\\\\[a-z0-9])",
    "email address": r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    "credential-shaped value": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)",
    "credential in URL": r"(?i)(?:[?&](?:api[_-]?key|token|secret|password)=|https?://[^/\s]+:[^/\s]+@)",
    "local or private endpoint": r"(?i)https?://(?:localhost|127\.|10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)",
    "unresolved slash command": r'(?im)(?:^|"text"\s*:\s*")/[a-z][a-z0-9-]*(?:\s|"|$)',
}


def privacy_findings(text):
    """Return categories, never the potentially sensitive matching values."""
    return [label for label, pattern in PATTERNS.items() if re.search(pattern, text)]


def validate_public_url(value):
    url = urlparse(value)
    host = url.hostname or ""
    if (
        value != value.strip()
        or url.scheme != "https"
        or url.username
        or url.password
        or url.query
        or url.fragment
        or url.port not in (None, 443)
        or not re.fullmatch(r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}", host)
        or host.endswith(
            (".local", ".localhost", ".internal", ".lan", ".home", ".test", ".invalid")
        )
        or privacy_findings(value)
    ):
        raise ValueError(
            "Website buttons need public HTTPS hostnames without account parameters"
        )


def validate_catalog(catalog):
    slug = re.compile(r"^[a-z][a-z0-9-]*$")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-z0-9.]+)?", catalog.get("version", "")):
        raise ValueError("Catalog version must be a portable release identifier")
    findings = privacy_findings(json.dumps(catalog, ensure_ascii=False))
    if findings:
        raise ValueError("Catalog privacy review required: " + ", ".join(findings))
    if not slug.fullmatch(catalog.get("id", "")):
        raise ValueError("Catalog needs a portable lowercase id")
    if not isinstance(catalog.get("name"), str) or not catalog["name"].strip():
        raise ValueError("Catalog needs a name")
    prompts = catalog.get("prompts")
    pages = catalog.get("pages")
    if (
        not isinstance(prompts, dict)
        or not prompts
        or not isinstance(pages, list)
        or not pages
    ):
        raise ValueError("Catalog needs prompts and pages")
    page_ids = [page.get("id") for page in pages]
    if page_ids[0] != "home" or len(set(page_ids)) != len(page_ids):
        raise ValueError("Home must be first and page ids must be unique")
    for prompt_id, prompt in prompts.items():
        if "icon" in prompt and not artwork.valid_icon(prompt["icon"]):
            raise ValueError("Invalid prompt icon")
        if not slug.fullmatch(prompt_id) or not all(
            isinstance(prompt.get(k), str) and prompt[k].strip()
            for k in ("title", "text")
        ):
            raise ValueError("Invalid prompt")
        findings = privacy_findings(prompt["text"])
        if findings or "\ufffd" in prompt["text"]:
            raise ValueError(
                f"{prompt_id}: unsafe or damaged text ({', '.join(findings)})"
            )
    graph = {}
    used_prompts = set()
    for page in pages:
        if not isinstance(page["id"], str) or not slug.fullmatch(page["id"]):
            raise ValueError("Invalid page id")
        if not re.fullmatch(
            r"#[0-9a-fA-F]{6}", page.get("color", "")
        ) or not artwork.valid_icon(page.get("symbol")):
            raise ValueError("Invalid page color or symbol")
        occupied = set() if page["id"] == "home" else {"0,0"}
        graph[page["id"]] = []
        for button in page.get("buttons", []):
            slot = button.get("slot", "")
            if not re.fullmatch(r"[0-4],[0-2]", slot) or slot in occupied:
                raise ValueError(
                    f"{page['id']}: duplicate, reserved or invalid button slot"
                )
            occupied.add(slot)
            labels = button.get("label")
            if (
                not isinstance(labels, list)
                or not 1 <= len(labels) <= 2
                or any(
                    not isinstance(label, str) or not 1 <= len(label) <= 12
                    for label in labels
                )
            ):
                raise ValueError("Button labels need one or two short lines")
            if button.get("kind") == "prompt" and button.get("prompt") in prompts:
                used_prompts.add(button["prompt"])
            elif (
                button.get("kind") == "folder"
                and button.get("page") in page_ids
                and button["page"] != "home"
            ):
                graph[page["id"]].append(button["page"])
            elif button.get("kind") == "website":
                validate_public_url(button.get("url", ""))
            elif (
                button.get("kind") == "hotkey"
                and button.get("shortcut") in BROWSER_KEYS
            ):
                pass
            else:
                raise ValueError("Unsupported action or unresolved button target")
    visited = set()

    def visit(page_id, ancestors):
        if page_id in ancestors:
            raise ValueError("Folder navigation must not contain cycles")
        visited.add(page_id)
        for child in graph[page_id]:
            visit(child, ancestors | {page_id})

    visit("home", set())
    if visited != set(page_ids) or used_prompts != set(prompts):
        raise ValueError("Every page and prompt must be reachable")


def identifier(value):
    return str(uuid.uuid5(NAMESPACE, value)).upper()


def icon_svg(color, symbol, labels=None, folder=False):
    return artwork.icon_svg(color, symbol, labels, folder=folder)


def button_style(catalog, page, button):
    if button["kind"] == "back":
        return page["color"], "back"
    if button["kind"] == "folder":
        target = next(item for item in catalog["pages"] if item["id"] == button["page"])
        return target["color"], target["symbol"]
    if button["kind"] in ("website", "hotkey"):
        return page["color"], artwork.pick_icon(
            " ".join(button["label"]), "panels-top-left"
        )
    prompt = catalog["prompts"][button["prompt"]]
    symbol = prompt.get("icon") or artwork.pick_icon(prompt["title"], page["symbol"])
    if page["id"] == "home":
        for candidate in catalog["pages"][1:]:
            if any(
                item.get("prompt") == button["prompt"] for item in candidate["buttons"]
            ):
                return candidate["color"], symbol
    return page["color"], symbol


def build_profile(catalog):
    validate_catalog(catalog)
    root = identifier(catalog["id"]) + ".sdProfile"
    pages = {
        page["id"]: identifier(catalog["id"] + "/" + page["id"])
        for page in catalog["pages"]
    }
    files = {}

    def emit(name, data):
        files[name] = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode(
            "utf-8"
        )

    emit(
        root + "/manifest.json",
        {
            "AppIdentifier": "",
            "Device": {"Model": "20GBA9901"},
            "Name": catalog["name"],
            "Pages": {
                "Current": pages["home"],
                "Default": pages["home"],
                "Pages": [pages["home"]],
            },
            "Version": "3.0",
        },
    )
    for page in catalog["pages"]:
        base = root + "/Profiles/" + pages[page["id"]]
        buttons = list(page["buttons"])
        if page["id"] != "home":
            buttons.insert(0, {"slot": "0,0", "kind": "back", "label": ["BACK"]})
        actions = {}
        for button in buttons:
            kind = button["kind"]
            if kind == "folder":
                action_uuid, name = (
                    "com.elgato.streamdeck.profile.openchild",
                    "Create Folder",
                )
                settings = {"ProfileUUID": pages[button["page"]]}
            elif kind == "back":
                action_uuid, name = (
                    "com.elgato.streamdeck.profile.backtoparent",
                    "Parent folder",
                )
                settings = {}
            elif kind == "website":
                action_uuid, name = "com.elgato.streamdeck.system.website", "Website"
                settings = {"openInBrowser": True, "path": button["url"]}
            elif kind == "hotkey":
                action_uuid, name = "com.elgato.streamdeck.system.hotkey", "Hotkey"
                key, shift = BROWSER_KEYS[button["shortcut"]]
                settings = {
                    "Hotkeys": [
                        {
                            "KeyCmd": False,
                            "KeyCtrl": True,
                            "KeyOption": False,
                            "KeyShift": shift,
                            "NativeCode": key,
                            "QTKeyCode": key,
                            "VKeyCode": key,
                            "KeyModifiers": 3 if shift else 1,
                        }
                    ]
                }
            else:
                action_uuid, name = "com.elgato.streamdeck.system.text", "Text"
                settings = {
                    "Hotkey": {
                        "KeyModifiers": 0,
                        "QTKeyCode": 33554431,
                        "VKeyCode": -1,
                    },
                    "isSendingEnter": False,
                    "isTypingMode": False,
                    "pastedText": GUARD + catalog["prompts"][button["prompt"]]["text"],
                }
            color, symbol = button_style(catalog, page, button)
            image_path = "Images/key-" + button["slot"].replace(",", "-") + ".svg"
            files[base + "/" + image_path] = icon_svg(
                color, symbol, folder=kind == "folder"
            ).encode("utf-8")
            actions[button["slot"]] = {
                "ActionID": identifier(
                    catalog["id"] + "/" + page["id"] + "/" + button["slot"]
                ),
                "LinkedTitle": True,
                "Name": name,
                "Plugin": {"Name": name, "UUID": action_uuid, "Version": "1.0"},
                "Resources": None,
                "Settings": settings,
                "State": 0,
                "States": [
                    {
                        "FontFamily": "Arial",
                        "FontSize": 10,
                        "FontStyle": "Bold",
                        "FontUnderline": False,
                        "Image": image_path,
                        "OutlineThickness": 0,
                        "ShowTitle": True,
                        "Title": "\n".join(button["label"]),
                        "TitleAlignment": "bottom",
                        "TitleColor": "#f8fafc",
                    }
                ],
                "UUID": action_uuid,
            }
        emit(
            base + "/manifest.json",
            {
                "Controllers": [{"Type": "Keypad", "Actions": actions}],
                "Icon": "",
                "Name": page["title"],
            },
        )
    files[root + "/Icon-LICENSE.txt"] = (ROOT / "assets/icons/LICENSE.txt").read_bytes()
    files[root + "/LICENSE.txt"] = (ROOT / "LICENSE").read_bytes()
    return files


def package_profile(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path, data in sorted(files.items()):
            if path.startswith("/") or ".." in path.split("/") or "\\" in path:
                raise ValueError("Archive path must be relative and portable")
            info = zipfile.ZipInfo(path, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(
                info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
            )
    return buffer.getvalue()


def layout_svg(catalog, page):
    buttons = list(page["buttons"])
    if page["id"] != "home":
        buttons.insert(0, {"slot": "0,0", "kind": "back", "label": ["BACK"]})
    tiles = ""
    for button in buttons:
        x, y = (int(part) for part in button["slot"].split(","))
        color, symbol = button_style(catalog, page, button)
        inner = icon_svg(
            color, symbol, button["label"], folder=button["kind"] == "folder"
        )
        tiles += f'<g transform="translate({22 + x * 156},{76 + y * 156})">{inner}</g>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="812" height="564" viewBox="0 0 812 564">'
        f'<rect width="812" height="564" rx="24" fill="#0E151E"/>'
        f'<text x="24" y="43" fill="#F4F0E8" font-family="Arial,sans-serif" font-size="25" font-weight="700">{html.escape(catalog["name"] + " / " + page["title"])}</text>'
        f'{tiles}<text x="24" y="552" fill="#A4B1C2" font-family="Arial,sans-serif" font-size="11">Layout guide. Text buttons paste; links open in your default browser; shortcuts act on the focused app.</text></svg>'
    )


def compile_repository(root=ROOT, check=False):
    root = root.resolve()
    expected = {}
    gallery = []
    sources = sorted((root / "profiles").glob("*.json"))
    if not sources:
        raise ValueError("At least one profile catalog is required")
    catalog_ids = set()
    for source in sources:
        catalog = json.loads(source.read_text(encoding="utf-8"))
        files = build_profile(catalog)
        if catalog["id"] in catalog_ids:
            raise ValueError("Catalog ids must be unique across source files")
        catalog_ids.add(catalog["id"])
        filename = catalog["id"] + "-" + catalog["version"] + ".streamDeckProfile"
        expected["dist/" + filename] = package_profile(files)
        lines = [
            f"# {catalog['name']}: button guide",
            "",
            catalog["description"],
            "",
            "Each prompt is prefixed with the shared scope, tool-availability and approval guard in `scripts/build.py`. Text buttons paste without Enter. Website buttons open the default browser; shortcut buttons act immediately on the focused application.",
            "",
        ]
        for page in catalog["pages"]:
            expected[f"docs/previews/{catalog['id']}-{page['id']}.svg"] = layout_svg(
                catalog, page
            ).encode("utf-8")
            title = html.escape(catalog["name"] + " / " + page["title"])
            url = f"previews/{catalog['id']}-{page['id']}.svg"
            gallery.append(
                f'<figure><a href="{url}"><img src="{url}" alt="{title}" width="812" height="564"></a><figcaption>{title}</figcaption></figure>'
            )
            lines += [
                f"## {page['title']}",
                "",
                f"![{page['title']} layout](previews/{catalog['id']}-{page['id']}.svg)",
                "",
            ]
            for button in page["buttons"]:
                if button["kind"] in ("website", "hotkey"):
                    lines += [
                        f"### {' / '.join(button['label'])}",
                        "",
                        f"Button `{button['slot']}`: {button.get('url', button.get('shortcut'))}.",
                        "",
                    ]
                if button["kind"] != "prompt":
                    continue
                prompt = catalog["prompts"][button["prompt"]]
                lines += [
                    f"### {' / '.join(button['label'])}: {prompt['title']}",
                    "",
                    f"Button `{button['slot']}` (column,row; zero based).",
                    "",
                    prompt["text"],
                    "",
                ]
        expected[f"docs/{catalog['id']}.md"] = (
            "\n".join(lines).rstrip() + "\n"
        ).encode("utf-8")
        print(
            f"{catalog['name']}: {len(catalog['prompts'])} unique prompts, {len(catalog['pages'])} pages, {len(files)} packaged files"
        )
    ring_sources = sorted((root / "rings").glob("*.json"))
    if ring_sources:
        import ring

        for source in ring_sources:
            catalog = json.loads(source.read_text(encoding="utf-8"))
            if catalog["id"] in catalog_ids:
                raise ValueError("Catalog ids must be unique across devices")
            catalog_ids.add(catalog["id"])
            files = ring.build_ring(catalog)
            navigation = ring.navigation_pages(catalog)
            nav_lookup = {page["id"]: page for page in navigation}
            expected[f"dist/{catalog['id']}-{catalog['version']}.lp5"] = (
                package_profile(files)
            )
            lines = [
                f"# {catalog['name']}: action guide",
                "",
                catalog["description"],
                "",
                f"{len(catalog['folders'])} source categories across {len(navigation)} navigation pages including Home. Home has at most 8 controls; action folders have at most 9. When needed, More workflows opens the remaining categories without removing any action.",
                "",
                "Text actions wait one second, then paste a prompt without pressing Enter. Windows shortcuts act immediately. Folder navigation is supplied by Logi Options+.",
                "",
            ]
            for nav_page in navigation:
                page_id = nav_page["id"]
                title = catalog["name"] + " / " + nav_page["title"]
                preview = f"{catalog['id']}-{page_id}.svg"
                expected["docs/previews/" + preview] = ring.layout_svg(
                    catalog, nav_page
                ).encode("utf-8")
                gallery.append(
                    f'<figure><a href="previews/{preview}"><img src="previews/{preview}" alt="{html.escape(title)}" width="900" height="850"></a><figcaption>{html.escape(title)}</figcaption></figure>'
                )
                lines += [
                    "## " + nav_page["title"],
                    "",
                    f"![{title}](previews/{preview})",
                    "",
                ]
                for i, action in enumerate(nav_page["items"], 1):
                    if action["kind"] == "folder":
                        target = nav_lookup[action["page"]]
                        description = f"Open [{target['title']}](previews/{catalog['id']}-{target['id']}.svg)."
                    else:
                        description = action.get(
                            "text",
                            "Shortcut: "
                            + ring.SHORTCUTS.get(action.get("shortcut"), ""),
                        )
                    lines += [f"### {i}. {action['title']}", "", description, ""]
            expected[f"docs/{catalog['id']}.md"] = (
                "\n".join(lines).rstrip() + "\n"
            ).encode("utf-8")
            print(
                f"{catalog['name']}: {sum(len(f['actions']) for f in catalog['folders'])} actions, {len(catalog['folders'])} categories, {len(navigation)} navigation pages"
            )
    expected["docs/gallery.html"] = (
        '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Ring &amp; Deck: all layouts</title><style>body{margin:0;padding:32px;background:#07101c;color:#f8fafc;font:16px/1.6 Arial,sans-serif}main{max-width:1700px;margin:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr));gap:24px}figure{margin:0}img{width:100%;height:auto}a:focus-visible{outline:3px solid #38bdf8}figcaption{color:#b6c2d1}h1{line-height:1.2}</style>"
        '<main><h1>Ring &amp; Deck</h1><p>Three Stream Deck workflows. Three Actions Ring workflows. Refined controls for focused work.</p><p>Generated layout guides, not hardware screenshots. Select a layout to inspect it at full size.</p><div class="grid">'
        + "".join(gallery)
        + "</div></main></html>\n"
    ).encode("utf-8")
    checksums = "".join(
        hashlib.sha256(data).hexdigest() + "  " + Path(name).name + "\n"
        for name, data in expected.items()
        if name.startswith("dist/")
    )
    expected["dist/SHA256SUMS.txt"] = checksums.encode("ascii")
    inventory_path = root / ".generated-files.json"
    previous = (
        json.loads(inventory_path.read_text(encoding="utf-8"))
        if inventory_path.is_file()
        else []
    )
    if not isinstance(previous, list) or any(
        not isinstance(name, str)
        or not re.fullmatch(
            r"(?:dist/[a-z0-9.-]+\.(?:streamDeckProfile|lp5)|dist/SHA256SUMS\.txt|docs/[a-z0-9-]+\.md|docs/gallery\.html|docs/previews/[a-z0-9-]+\.svg)",
            name,
        )
        or not (root / name).resolve().is_relative_to(root)
        for name in previous
    ):
        raise ValueError("Invalid generated-file inventory")
    discovered = {
        path.relative_to(root).as_posix()
        for pattern in ("dist/*.streamDeckProfile", "dist/*.lp5", "docs/previews/*.svg")
        for path in root.glob(pattern)
    }
    stale = sorted(
        name
        for name in (set(previous) | discovered) - set(expected)
        if (root / name).exists()
    )
    if stale:
        raise ValueError(
            "Stale generated files remain: "
            + ", ".join(stale)
            + ". Review and archive these files outside the repository, then rebuild."
        )
    expected[".generated-files.json"] = (
        json.dumps(sorted(expected), indent=2) + "\n"
    ).encode("utf-8")
    for name, data in expected.items():
        target = root / name
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"Generated path escapes the repository: {name}")
        if check:
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError(
                    f"Generated file is missing or stale: {name}. Run python scripts/build.py"
                )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(
        "Generated files verified."
        if check
        else "Packages and documentation generated."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Reject missing or stale generated output"
    )
    arguments = parser.parse_args()
    compile_repository(check=arguments.check)
