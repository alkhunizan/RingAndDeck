"""Compile portable Logitech Actions Ring catalogs into native LP5 files."""

import base64
import html
import json
import math
from pathlib import Path
import re
import subprocess
import uuid

import artwork
from build import GUARD, privacy_findings

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = uuid.UUID("5583eebf-0a46-4afd-a774-45e92b899816")
SHORTCUTS = {
    "dictate": "Windows+KeyH___67699721___Win+H___",
    "capture": "Windows+Shift+KeyS___67699721___Win+Shift+S___",
    "clipboard": "Windows+KeyV___67699721___Win+V___",
    "plain-paste": "ControlOrCommand+Shift+KeyV___67699721___Ctrl+Shift+V___",
    "files": "Windows+KeyE___67699721___Win+E___",
    "task-view": "Windows+Tab___67699721___Win+Tab___",
    "snap-layout": "Windows+KeyZ___67699721___Win+Z___",
}
SERVICE = "Loupedeck.Service."
LAYOUT = SERVICE + "Devices.Loupedeck7Devices."
APPLICATION_MODE = "System"
HOME_SLOTS = 8
FOLDER_SLOTS = 9


def uid(name):
    return uuid.uuid5(NAMESPACE, name).hex.upper()


def validate_ring(catalog):
    slug = re.compile(r"^[a-z][a-z0-9-]*$")
    if not slug.fullmatch(catalog.get("id", "")) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[a-z0-9.]+)?", catalog.get("version", "")
    ):
        raise ValueError("Invalid ring identity or version")
    if privacy_findings(json.dumps(catalog, ensure_ascii=False)):
        raise ValueError("Ring contains private or installation-specific content")
    folders = catalog.get("folders", [])
    if not 1 <= len(folders) <= 9:
        raise ValueError("Ring needs one to nine folders")
    folder_ids = set()
    action_ids = set()
    for folder in folders:
        if not slug.fullmatch(folder["id"]) or folder["id"] in folder_ids:
            raise ValueError("Duplicate or invalid folder id")
        folder_ids.add(folder["id"])
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", folder["color"]):
            raise ValueError("Invalid ring color")
        artwork.glyph(folder["icon"])
        if not 1 <= len(folder["actions"]) <= 9:
            raise ValueError("Folder needs one to nine actions")
        for action in folder["actions"]:
            if not slug.fullmatch(action["id"]) or action["id"] in action_ids:
                raise ValueError("Duplicate or invalid action id")
            action_ids.add(action["id"])
            if not action.get("title", "").strip():
                raise ValueError("Action needs a title")
            if action["kind"] == "prompt":
                if not action.get("text", "").strip():
                    raise ValueError("Prompt needs text")
            elif action["kind"] == "hotkey":
                if action.get("shortcut") not in SHORTCUTS:
                    raise ValueError("Unsupported shortcut")
            else:
                raise ValueError("Unsupported ring action")


def navigation_pages(catalog):
    """Keep nine-action categories intact within the eight-slot Home limit."""
    validate_ring(catalog)
    first = catalog["folders"][0]
    pages = [
        {
            "id": "home",
            "name": "home",
            "title": "Home",
            "color": first["color"],
            "icon": "folder-open",
            "items": [
                {
                    "kind": "folder",
                    "page": folder["id"],
                    "title": folder["title"],
                    "color": folder["color"],
                    "icon": folder["icon"],
                }
                for folder in catalog["folders"]
            ],
        }
    ]
    pages += [
        {
            "id": folder["id"],
            "name": "folder/" + folder["id"],
            "title": folder["title"],
            "color": folder["color"],
            "icon": folder["icon"],
            "items": [
                dict(action, color=folder["color"]) for action in folder["actions"]
            ],
        }
        for folder in catalog["folders"]
    ]
    home = pages[0]
    if len(home["items"]) > HOME_SLOTS:
        pages.append(
            {
                "id": "home-more",
                "name": "overflow/home",
                "title": "More workflows",
                "color": home["color"],
                "icon": "folder-open",
                "items": home["items"][HOME_SLOTS - 1 :],
            }
        )
        home["items"] = home["items"][: HOME_SLOTS - 1] + [
            {
                "kind": "folder",
                "page": "home-more",
                "title": "More workflows",
                "color": home["color"],
                "icon": "folder-open",
            }
        ]
    if len({page["id"] for page in pages}) != len(pages):
        raise ValueError("Category ids conflict with generated navigation pages")
    return pages


def icon_jobs(catalog, pages):
    jobs = {}
    for page in pages[1:]:
        jobs["folder/" + page["id"]] = artwork.icon_svg(
            page["color"], page["icon"], folder=True, ring=True
        )
    for folder in catalog["folders"]:
        for action in folder["actions"]:
            icon = action.get("icon") or artwork.pick_icon(
                action["title"], folder["icon"]
            )
            jobs["action/" + action["id"]] = artwork.icon_svg(
                folder["color"], icon, ring=True
            )
    return jobs


def build_ring(catalog):
    pages = navigation_pages(catalog)
    page_lookup = {page["id"]: page for page in pages}
    jobs = icon_jobs(catalog, pages)
    result = subprocess.run(
        ["node", str(ROOT / "scripts/render-icons.cjs")],
        input=json.dumps(jobs),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    images = {
        name: base64.b64decode(data) for name, data in json.loads(result.stdout).items()
    }
    files = {}

    def emit(name, value):
        files[name] = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode(
            "utf-8"
        )

    def identity(name):
        return uid(catalog["id"] + "/" + name)

    def control(index, ref):
        return {
            "$type": LAYOUT + "ProfileLayoutControl7, LoupedeckService",
            "controlId": index,
            "pressAction": ref,
            "rotateAction": None,
        }

    def page(name, title, controls):
        return {
            "$type": LAYOUT + "ProfileLayoutPage7, LoupedeckService",
            "name": identity(name),
            "displayName": title,
            "description": None,
            "controls": controls,
        }

    def parameters(key, value):
        return {
            "$type": "Loupedeck.ActionEditorActionParameters, PluginApi",
            "parameters": {
                "$type": "Loupedeck.StringDictionaryNoCase, PluginApi",
                key: value,
            },
            "count": 1,
        }

    def command(ref, title, template, params, group):
        return {
            "$type": SERVICE + "ApplicationProfileCommand, LoupedeckService",
            "isCommand": True,
            "name": ref,
            "templateActionName": "$@Generic___@" + template,
            "actionParameters": params,
            "displayName": title,
            "description": title,
            "groupName": group,
            "superGroupName": "@navigation" if template == "OpenFolder" else "@macro",
            "isProfileAction": True,
            "isMultiState": False,
            "isResetCommand": False,
            "adjustmentName": None,
            "states": None,
        }

    def add_icon(ref, key, title):
        png = images[key]
        files["ActionImages/" + ref + ".png"] = png
        emit(
            "ActionIcons/" + ref + ".ict",
            {
                "backgroundColor": 4279442213,
                "items": [
                    {
                        "$type": SERVICE + "ActionIconImageItem, LoupedeckShared",
                        "image": base64.b64encode(png).decode(),
                        "imageFileName": "icon.png",
                        "imageColor": 4294967295,
                        "imageRotation": "None",
                        "isVisible": True,
                        "itemType": "Image",
                        "area": {
                            "x": 0,
                            "y": 0,
                            "width": 100,
                            "height": 100,
                            "isFullScreen": True,
                        },
                    },
                    {
                        "$type": SERVICE + "ActionIconTextItem, LoupedeckShared",
                        "text": title,
                        "textColor": 4294967295,
                        "fontSize": 5,
                        "fontName": "Segoe UI",
                        "isVisible": False,
                        "itemType": "Text",
                        "area": {
                            "x": 0,
                            "y": 70,
                            "width": 100,
                            "height": 25,
                            "isFullScreen": False,
                        },
                    },
                ],
            },
        )

    profile_id = identity("profile")
    workspace_id = identity("workspace")
    macros = []
    commands = []
    preview = []
    for nav_page in pages[1:]:
        folder_id = identity(nav_page["name"])
        ref = "$@Generic___@ProfileAction___" + folder_id
        commands.append(
            command(
                ref,
                nav_page["title"],
                "OpenFolder",
                parameters("folderName", folder_id),
                "Folders",
            )
        )
        add_icon(ref, "folder/" + nav_page["id"], nav_page["title"])
    for folder in catalog["folders"]:
        for action in folder["actions"]:
            action_id = identity("action/" + action["id"])
            if action["kind"] == "prompt":
                ref = "$@Generic___@Macro___" + action_id
                editor_id = identity("text/" + action["id"])
                text = GUARD + action["text"]
                macros.append(
                    {
                        "$type": SERVICE
                        + "ApplicationProfileMacroCommand, LoupedeckService",
                        "isCommand": True,
                        "name": action_id,
                        "displayName": action["title"],
                        "description": text,
                        "groupName": folder["title"],
                        "superGroupName": "@macro",
                        "supportedOs": "Win",
                        "supportedModes": [],
                        "showAsSingleAction": False,
                        "actionEditorCommands": [
                            {
                                "$type": SERVICE
                                + "MacroActionEditorCommand, LoupedeckService",
                                "name": editor_id,
                                "templateName": "$@Generic___@SendText",
                                "actionParameters": {
                                    "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.String, System.Private.CoreLib]], System.Private.CoreLib",
                                    "text": text,
                                    "useClipboard": "true",
                                },
                            }
                        ],
                        "isMultiState": False,
                        "actions": ["$@Generic___@Sleep___1000", editor_id],
                    }
                )
            else:
                ref = "$@Generic___@ProfileAction___" + action_id
                commands.append(
                    command(
                        ref,
                        action["title"],
                        "KeyboardKey",
                        parameters("keyboardKey", SHORTCUTS[action["shortcut"]]),
                        folder["title"],
                    )
                )
            add_icon(ref, "action/" + action["id"], action["title"])
    native_pages = []
    for nav_page in pages:
        controls = []
        for index, item in enumerate(nav_page["items"]):
            if item["kind"] == "folder":
                ref = "$@Generic___@ProfileAction___" + identity(
                    page_lookup[item["page"]]["name"]
                )
                image_key = "folder/" + item["page"]
            else:
                prefix = (
                    "$@Generic___@Macro___"
                    if item["kind"] == "prompt"
                    else "$@Generic___@ProfileAction___"
                )
                ref = prefix + identity("action/" + item["id"])
                image_key = "action/" + item["id"]
            controls.append(control(index, ref))
            if nav_page["id"] == "home":
                preview.append(
                    {
                        "controlId": index,
                        "actionName": ref,
                        "displayName": item["title"],
                        "description": "Open " + item["title"],
                        "image": base64.b64encode(images[image_key]).decode(),
                    }
                )
        native_pages.append(page(nav_page["name"], nav_page["title"], controls))
    workspace = {
        "$type": LAYOUT + "ProfileLayoutWorkspace7, LoupedeckService",
        "name": workspace_id,
        "displayName": catalog["name"],
        "description": catalog["description"],
        "pressPages": [native_pages[0]],
        "rotatePages": [
            page("dial", "Dial Page", [control(i, None) for i in range(8)])
        ],
    }
    layout = {
        "$type": LAYOUT + "ProfileLayout7, LoupedeckService",
        "deviceType": "Loupedeck72",
        "profileFlags": "None",
        "layoutModes": [
            {
                "$type": LAYOUT + "ProfileLayoutMode7, LoupedeckService",
                "deviceType": "Loupedeck72",
                "modeName": APPLICATION_MODE,
                "parentModeName": None,
                "actions": None,
                "dynamicButtonPages": None,
                "dynamicEncoderPages": None,
                "workspaces": [workspace],
                "homeWorkspaceName": workspace_id,
            }
        ],
        "folderPages": native_pages[1:],
    }
    profile = {
        "$type": SERVICE + "ApplicationProfile, LoupedeckService",
        "name": profile_id,
        "profileFlags": "None",
        "displayName": catalog["name"],
        "description": catalog["description"],
        "deviceType": "Loupedeck72",
        "applicationName": "@_defaultwin",
        "nativePluginName": "DefaultWin",
        "hasNativePlugin": True,
        "additionalNativePluginNames": [],
        "lastModifiedTimeUtc": "2026-09-24T00:00:00Z",
        "profileSettings": {
            "$type": "Loupedeck.DictionaryNoCase`1[[System.String, System.Private.CoreLib]], PluginApi"
        },
        "actionImages90": None,
        "actionImages60": None,
        "wheelImages": None,
        "actionColors": None,
        "layout": layout,
        "macroCommands": macros,
        "macroAdjustments": [],
        "profileCommands": [],
        "profileAdjustments": [],
        "conversionHistory": "",
        "packageName": profile_id,
        "packageVersion": catalog["version"],
        "profileActions": commands,
    }
    emit("ProfileInfo.json", profile)
    emit(
        "ApplicationInfo.json",
        {
            "$type": SERVICE + "SupportedApplicationInfo, LoupedeckService",
            "name": "@_defaultwin",
            "displayName": "System plugin",
            "description": None,
            "deviceType": "Loupedeck72",
            "nativePluginName": "DefaultWin",
            "hasNativePlugin": True,
            "processOrBundleName": None,
            "modes": [
                {
                    "$type": SERVICE + "ApplicationMode, LoupedeckService",
                    "name": APPLICATION_MODE,
                    "parentModeName": None,
                    "displayName": "System",
                }
            ],
            "defaultProfileName": profile_id,
            "isEnabled": True,
        },
    )
    files["ApplicationIcon.png"] = images["folder/" + catalog["folders"][0]["id"]]
    emit("metadata/AdvancedInfo.json", {"additionalPluginNames": []})
    emit(
        "metadata/ProfilePreview.json",
        {
            "buttonPages": preview,
            "encoderPages": [
                {
                    "controlId": i,
                    "actionName": None,
                    "displayName": None,
                    "description": None,
                    "image": None,
                }
                for i in range(8)
            ],
        },
    )
    files["metadata/LoupedeckPackage.yaml"] = (
        f"type: Profile5\nname: {profile_id}\ndisplayName: "
        + json.dumps(catalog["name"])
        + "\nversion: "
        + catalog["version"]
        + "\ndescription: "
        + json.dumps(catalog["description"])
        + "\n"
    ).encode()
    files["metadata/Icon-LICENSE.txt"] = (
        ROOT / "assets/icons/LICENSE.txt"
    ).read_bytes()
    files["metadata/LICENSE.txt"] = (ROOT / "LICENSE").read_bytes()
    return files


def layout_svg(catalog, nav_page=None):
    nav_page = navigation_pages(catalog)[0] if nav_page is None else nav_page
    items = nav_page["items"]
    title = catalog["name"] + " / " + nav_page["title"]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="850" viewBox="0 0 900 850"><rect width="900" height="850" rx="28" fill="#0E151E"/><text x="36" y="48" fill="#F4F0E8" font-family="Arial,sans-serif" font-size="25" font-weight="700">{html.escape(title)}</text><circle cx="450" cy="425" r="278" fill="none" stroke="#293646"/><circle cx="450" cy="425" r="102" fill="#18232F" stroke="#435163"/><text x="450" y="418" text-anchor="middle" fill="#E5B879" font-family="Arial,sans-serif" font-size="14" letter-spacing="2">ACTIONS RING</text><text x="450" y="447" text-anchor="middle" fill="#F4F0E8" font-family="Arial,sans-serif" font-size="21">Native navigation</text>'
    for i, item in enumerate(items):
        slots = HOME_SLOTS if nav_page["id"] == "home" else FOLDER_SLOTS
        angle = -math.pi / 2 + i * 2 * math.pi / slots
        x = 450 + 270 * math.cos(angle)
        y = 425 + 270 * math.sin(angle)
        color = item["color"]
        symbol = item.get("icon") or artwork.pick_icon(item["title"])
        svg += (
            f'<g transform="translate({x - 54:.2f},{y - 54:.2f})"><svg width="108" height="108" viewBox="0 0 144 144">'
            + artwork.icon_svg(color, symbol, ring=True)
            + "</svg></g>"
        )
        words = item["title"].split()
        lines = [item["title"]]
        if len(item["title"]) > 19:
            middle = (
                min(
                    range(1, len(words)),
                    key=lambda n: abs(
                        len(" ".join(words[:n])) - len(" ".join(words[n:]))
                    ),
                )
                if len(words) > 1
                else 1
            )
            lines = [" ".join(words[:middle]), " ".join(words[middle:])]
        for j, line in enumerate(lines):
            svg += f'<text x="{x:.2f}" y="{y + 72 + j * 19:.2f}" text-anchor="middle" fill="#F4F0E8" font-family="Arial,sans-serif" font-size="16" font-weight="600">{html.escape(line)}</text>'
    return (
        svg
        + '<text x="36" y="820" fill="#A4B1C2" font-family="Arial,sans-serif" font-size="13">Generated layout guide. Native overlay geometry and labels may differ.</text></svg>'
    )
