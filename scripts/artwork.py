"""Shared, scalable artwork for native controls and honest layout previews."""

import hashlib
import html
from pathlib import Path
import re

ASSETS = Path(__file__).resolve().parents[1] / "assets/icons"
PALETTE = [
    "#9FAEF5",
    "#7DCEC2",
    "#E5B879",
    "#AE9CE1",
    "#E697A5",
    "#94C3DD",
    "#B6CC92",
    "#DDAA83",
    "#A8B8C9",
]
ALIASES = {
    "code": "blocks",
    "check": "shield-check",
    "search": "scan-search",
    "plan": "clipboard-list",
    "chat": "bot-message-square",
    "focus": "timer",
    "folder": "folder-open",
    "learn": "book-open",
    "branch": "git-compare-arrows",
}
RULES = [
    ("credential|account access|password|security|privacy", "key-round"),
    ("undo|revert|back|recover|resume|restart|reopen", "repeat-2"),
    ("migration|handoff|hand off|delegate", "package-open"),
    ("race|bug|debug|error|break|flake", "bug"),
    ("test|experiment|probe|assumption", "flask-conical"),
    ("verify|evidence|proof|prove|audit|source|facts", "microscope"),
    ("search|find|where", "scan-search"),
    ("map|context|orient|prime|framework", "map"),
    ("risk|harden|safe|stress|gate", "shield-check"),
    ("review|adversarial|opposite|argue|counter", "swords"),
    ("git|diff|rebase|branch|commit|worktree|merge", "git-compare-arrows"),
    ("write|draft|polish|voice|caption", "feather"),
    ("translate|language|tone|english", "languages"),
    ("speak|dictat|mic", "mic"),
    ("capture|screenshot|photo", "camera"),
    ("clipboard|copy", "copy-plus"),
    ("paste|compress|shorten|trim", "clipboard-minus"),
    ("time|focus|sprint|minutes|body double|timebox", "timer"),
    ("calendar|today|week|month|deadline", "calendar-days"),
    ("email|mail|reply|message", "mail"),
    ("client|proposal|payment|invoice", "handshake"),
    ("team|person|people|council|employee|owner", "users-round"),
    ("plan|task|checklist|list|priorit|done", "list-checks"),
    ("build|implement|code|fix", "hammer"),
    ("tool|automation|stack|environment|integrat|api", "network"),
    ("pattern|interface|architecture|structure", "blocks"),
    ("learn|explain|teach|mentor|simple", "book-open"),
    ("research|question|missing", "telescope"),
    ("report|document|release note|changelog|summary", "file-text"),
    ("table|metric|data", "table-2"),
    ("compare|decid|choose|trade|budget|cheaper", "scale"),
    ("content|campaign|social|publish|audience", "megaphone"),
    ("win|delivered|ship|release", "trophy"),
    ("goal|mission|finish|checkpoint", "flag"),
    ("save|memory|record|note|park", "notebook-pen"),
    ("next|start|first|step|continue", "footprints"),
    ("scale|insight|analytic|return|performance", "chart-no-axes-combined"),
    ("funnel|filter|waste", "funnel"),
    ("browser|tab|window|layout|zoom", "panels-top-left"),
    ("file|folder|drive", "folder-open"),
    ("ai|prompt|assistant|chat|agent", "bot-message-square"),
    ("improve|creative|idea|best", "sparkles"),
]


def pick_icon(text, fallback="sparkles"):
    for pattern, icon in RULES:
        if re.search(pattern, text, re.I):
            return icon
    return ALIASES.get(fallback, fallback)


def valid_icon(name):
    return isinstance(name, str) and (
        name == "back"
        or name in ALIASES
        or name in {p.stem for p in ASSETS.glob("*.svg")}
    )


def glyph(name):
    if name == "back":
        return '<path d="m10 5-7 7 7 7M3 12h18"/>'
    name = ALIASES.get(name, name)
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("Invalid icon name")
    source = (ASSETS / (name + ".svg")).read_text(encoding="utf-8")
    return source[source.index(">", source.index("<svg")) + 1 : source.rindex("</svg>")]


def icon_svg(color, symbol, labels=None, folder=False, ring=False):
    """A generous symbol area stays clear of the application's title overlay."""
    key = hashlib.sha256(
        (color + symbol + str(folder) + str(ring)).encode()
    ).hexdigest()[:10]
    radius = 70 if ring else 19
    shape = (
        f'<circle cx="72" cy="72" r="69" fill="url(#bg{key})"/>'
        if ring
        else f'<rect x="2" y="2" width="140" height="140" rx="{radius}" fill="url(#bg{key})"/>'
    )
    rim = (
        '<circle cx="72" cy="72" r="67.5"/>'
        if ring
        else '<rect x="3.5" y="3.5" width="137" height="137" rx="18"/>'
    )
    text = ""
    if labels:
        for i, label in enumerate(labels):
            y = 111 + i * 19 if len(labels) > 1 else 121
            text += f'<text x="72" y="{y}" text-anchor="middle" fill="#F4F0E8" font-family="Arial,sans-serif" font-size="14" font-weight="700">{html.escape(label)}</text>'
    motif = (
        '<circle cx="114" cy="23" r="2"/><circle cx="121" cy="23" r="2"/><circle cx="128" cy="23" r="2"/>'
        if folder and not ring
        else ""
    )
    symbol_y, symbol_size = (39, 66) if ring else (28, 60)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="144" height="144" viewBox="0 0 144 144">'
        f'<defs><linearGradient id="bg{key}" x2=".7" y2="1"><stop stop-color="#28313D"/><stop offset="1" stop-color="#131B25"/></linearGradient>'
        f'<radialGradient id="light{key}"><stop stop-color="{color}" stop-opacity=".18"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
        f'{shape}<g fill="none" stroke="{color}" stroke-opacity=".45" stroke-width="1.2">{rim}</g>'
        f'<circle cx="72" cy="62" r="57" fill="url(#light{key})"/>'
        f'<path d="M57 12h30" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
        f'<g fill="{color}" opacity=".85">{motif}</g>'
        f'<svg x="{(144 - symbol_size) / 2}" y="{symbol_y}" width="{symbol_size}" height="{symbol_size}" viewBox="0 0 24 24" fill="none" stroke="#F4F0E8" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{glyph(symbol)}</svg>'
        f"{text}</svg>"
    )
