"""Shared, scalable artwork for native controls and honest layout previews."""

from functools import cache
import html
import json
from pathlib import Path
import re

ASSETS = Path(__file__).resolve().parents[1] / "assets/icons"
COLOR_ASSETS = ASSETS.parent / "color-icons"
INK = "#111827"
WHITE = "#FFFFFF"
TITLE_ADVANCES = {
    character: units / 1000
    for characters, units in (
        ("ABCDHKNUR", 722),
        ("EPSVXY", 667),
        ("FLTZ", 611),
        ("GOQ", 778),
        ("J0123456789", 556),
        ("M", 833),
        ("W", 944),
        ("I /", 278),
        ("-", 333),
        ("+", 584),
    )
    for character in characters
}
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
    (r"\bgit\b|diff|rebase|branch|commit|worktree|merge", "git-compare-arrows"),
    ("write|draft|polish|voice|caption", "feather"),
    ("translate|language|tone|english", "languages"),
    (r"speak|dictat|\bmic\b|microphone", "mic"),
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
    (r"tool|automation|stack|environment|integrat|\bapi\b", "network"),
    ("pattern|interface|architecture|structure", "blocks"),
    ("learn|explain|teach|mentor|simple", "book-open"),
    ("research|question|missing", "telescope"),
    ("report|document|release note|changelog|summary", "file-text"),
    ("table|metric|data", "table-2"),
    ("compare|decid|choose|trade|budget|cheaper", "scale"),
    ("content|campaign|social|publish|audience", "megaphone"),
    (r"\bwin\b|delivered|ship|release", "trophy"),
    ("goal|mission|finish|checkpoint", "flag"),
    ("save|memory|record|note|park", "notebook-pen"),
    ("next|start|first|step|continue", "footprints"),
    ("scale|insight|analytic|return|performance", "chart-no-axes-combined"),
    ("funnel|filter|waste", "funnel"),
    ("browser|tab|window|layout|zoom", "panels-top-left"),
    ("file|folder|drive", "folder-open"),
    (r"\bai\b|prompt|assistant|chat|agent", "bot-message-square"),
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


@cache
def _color_manifest():
    return json.loads((COLOR_ASSETS / "manifest.json").read_text(encoding="utf-8"))


def _icon_name(name):
    name = ALIASES.get(name, name)
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("Invalid icon name")
    return name


def accent_for_symbol(name):
    return _color_manifest()[_icon_name(name)]["accent"]


@cache
def glyph(name):
    name = _icon_name(name)
    source = (COLOR_ASSETS / (name + ".svg")).read_text(encoding="utf-8")
    return source[source.index(">", source.index("<svg")) + 1 : source.rindex("</svg>")]


def title_font_size(labels):
    """Native 72px title size, shared with the double-size preview artwork."""
    # Arial Bold advances estimate a 132px line before native raster hinting.
    widest = max(
        (sum(TITLE_ADVANCES.get(character, 1) for character in label) for label in labels),
        default=0,
    )
    return max(8, min(10, int(66 / widest))) if widest else 10


def icon_svg(color, symbol, labels=None, folder=False, ring=False):
    """Familiar full-color objects share one native and preview composition."""
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("Invalid icon color")
    accent = accent_for_symbol(symbol)
    opening = '<svg xmlns="http://www.w3.org/2000/svg" width="144" height="144" viewBox="0 0 144 144">'
    if ring:
        surface = (
            '<circle cx="72" cy="72" r="69" fill="#F5F8FF"/>'
            f'<circle cx="72" cy="72" r="67" fill="none" stroke="{accent}" stroke-width="3"/>'
        )
        symbol_size = 86
        symbol_y = 29
        navigation = (
            f'<circle cx="111" cy="111" r="13.5" fill="{INK}"/>'
            f'<path d="m108 106 6 5-6 5" fill="none" stroke="{WHITE}" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round"/>'
            if folder else ""
        )
        text = ""
    else:
        surface = (
            f'<rect x="2" y="2" width="140" height="140" rx="19" fill="{INK}"/>'
            '<path d="M21 2h102a19 19 0 0 1 19 19v77H2V21A19 19 0 0 1 21 2Z" fill="#F5F8FF"/>'
            f'<path d="M3 98h138" stroke="{accent}" stroke-width="3"/>'
            '<rect x="2.75" y="2.75" width="138.5" height="138.5" rx="18.25" fill="none" stroke="#DDE5F1" stroke-width="1.5"/>'
        )
        symbol_size, symbol_y = 82, 10
        navigation = (
            f'<circle cx="124" cy="18" r="10.5" fill="{INK}"/>'
            f'<path d="m122 14 4 4-4 4" fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
            if folder else ""
        )
        text = ""
        font_size = title_font_size(labels or []) * 2
        for index, label in enumerate(labels or []):
            y = 134 - (len(labels) - index - 1) * font_size
            text += (
                f'<text x="72" y="{y}" text-anchor="middle" fill="{WHITE}" '
                f'font-family="Arial,sans-serif" font-size="{font_size}" font-weight="700">'
                f"{html.escape(label)}</text>"
            )
    symbol_x = (144 - symbol_size) / 2
    # Stream Deck renders SVG Tiny, which drops nested <svg>; place the 32px glyph with a transform.
    mark = (
        f'<g transform="translate({symbol_x:g} {symbol_y:g}) scale({symbol_size / 32:g})">'
        f"{glyph(symbol)}</g>"
    )
    return opening + surface + mark + navigation + text + "</svg>"
