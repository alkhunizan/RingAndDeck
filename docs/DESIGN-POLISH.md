# Alpha.3 visual candidate

Design review recorded on 2026-09-24 before publication. The reviewed artwork is now included in the alpha.3 prerelease. The MINI agent subsequently reported native Stream Deck Home rendering after the SVG fix; see [the separate evidence record](STREAM-DECK-ICON-FIX.md).

## What changed

All six profiles now use vivid, full-color Microsoft Fluent Emoji Flat illustrations. Clean pale icon fields keep the objects visible, and a navy title strip gives Stream Deck labels a consistent reading area. Actions Ring controls use centered artwork on pale circular fields. Folder and Back cues remain distinct from prompt actions.

The owner requested this colorful revision after reviewing the earlier warm artwork. Icon choices follow familiar meanings across both devices: a magnifying glass for search and review, a pen for writing, tools for building, a red lady beetle for debugging, a robot for AI, a light bulb for ideas, a calendar for scheduling, a stopwatch for focus, and a shield or key for security. Accents reinforce the action meaning; they do not change according to a control's position.

The original illustration colors are preserved. All 67 locally included SVG assets use a 32 by 32 viewBox and come from one pinned upstream revision. The [asset manifest](../assets/color-icons/manifest.json) records exact sources, SHA-256 hashes and semantic accents. Microsoft artwork is redistributed under its [MIT license](../assets/color-icons/LICENSE.txt); [the notice](../assets/color-icons/NOTICE.md) records provenance.

Native application labels remain Arial for compatibility. Stream Deck labels use the same sizing rule in native exports and guides: size 10 for most labels and 8 or 9 for longer labels, represented at double resolution in previews. The HTML showcases use locally bundled Source Sans 3, Spectral and IBM Plex Mono with their font licenses. The exported collection PNGs are vector layout compositions using Georgia and Arial. No external font request is required. Generated guides and native packages share the same artwork; the guides remain diagrams, not native application screenshots.

## What stayed the same

All prompt text, action labels, profile and action identifiers, shortcuts, timing, navigation and manual submission settings are preserved. The profiles contain no API client or API keys. The chosen AI app still manages credentials and submission.

## Evidence

- Asset acquisition checks passed: all 67 SVGs match their recorded SHA-256 hashes and have no scripts, external references, gradients, element IDs or embedded images.
- `npm run check` passes all 13 native tests and the deterministic generated-output check.
- Independent comparison against immutable public main commit `bf98287c53d034540ba4204ba4d220ffc9dc114c` verifies exact prompt text, labels, native IDs, hotkeys, guard settings and navigation across all six packages. The six artwork license replacements are individually verified against the source MIT bytes.
- All six archives pass SHA-256, ZIP integrity, safe paths and byte identity with a fresh build.
- All 262 Ring icons decode at 288 by 288 pixels and fit their circular crop. Every displayed Ring icon matches the native export.
- All 257 Deck glyphs clear the title strip. Arial Bold labels use sizes 8 to 10 and fit the key; white labels on navy have 17.74:1 contrast. This is a label measurement, not a blanket contrast claim for multicolor drawings.
- All 55 generated guides were rendered and visually reviewed; 887 measured text elements have no clipping or overlap findings.
- [Artwork study](design-polish/native-artwork-review.png) and [72px exported-artwork proof](design-polish/native-72px-proof.png) were regenerated and inspected for this revision.

The companion website gives each profile more space and preserves its image proportions in English and Arabic. At review time, it separated the then-local alpha.3 visuals from published alpha.2 downloads. That companion website work is separate from GitHub publication. Fresh format, lint, typecheck, 1,269 tests and production build pass. Browser DOM checks cover both project pages and languages at 375px and 1440px with correct direction and no horizontal overflow. All eight served artworks match the source hashes. Below-fold images remain lazy-loaded. Browser screenshot capture was unreliable, so the showcase PNGs were generated as complete vector layout compositions and visually inspected. Physical mobile review remains open.

## Acceptance still open

Alpha.3 has not been imported into Logi Options+. MINI reports that all three fixed Stream Deck profiles display their Home pictograms and titles in Stream Deck 7.6.0.23012. The tester also reported tight title spacing. Native action activation, folder/Back navigation, selection/hover states, physical controls and device-screen readability still need acceptance testing. Earlier Code Ring UI screenshots are historical alpha.1 evidence, not validation of this artwork.

Keep this build labeled alpha. Import it separately after backing up working profiles and test text actions in a blank scratch document. Follow [SETUP.md](SETUP.md). The published alpha.2 release and production website are unchanged.
