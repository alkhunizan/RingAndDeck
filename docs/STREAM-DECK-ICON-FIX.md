# Alpha.3 Stream Deck icon fix

Prepared 2026-09-24. This fix is included in the [alpha.3 prerelease](https://github.com/alkhunizan/RingAndDeck/releases/tag/v0.1.0-alpha.3). Earlier alpha.2 downloads remain available unchanged.

## Reported native finding

The MINI testing agent reported that the first colorful alpha.3 profiles imported into Stream Deck 7.6.0.23012, but their pictograms were blank. The image backgrounds, labels and folder chevrons remained visible. The glyph was embedded in a nested `svg` element, which that native renderer dropped even though browsers and Sharp displayed it.

The handoff source replaces the nested viewport with a translated and uniformly scaled `g` element. The 32 by 32 source drawings, geometry, colors, native labels, profile identifiers, prompts and action settings are unchanged. Ring packages use raster PNG artwork and are byte-identical to the preceding colorful candidate.

MINI reported importing all three rebuilt Stream Deck profiles without modifications into the virtual 15-key editor. All Home keys displayed their pictograms and titles. This is reported native configuration-UI evidence; it is not a new native test on the source-preparation machine or proof of physical-key behavior. This report does not establish folder/Back navigation, text paste, shortcut or website activation, AI-composer behavior, or hardware readability. Alpha.3 Ring imports remain unverified.

## Source and artifact verification

The full colorful handoff source, including the MINI fix, was imported into an isolated Git branch based on public main commit `bf98287c53d034540ba4204ba4d220ffc9dc114c`. The original handoff is preserved.

- `npm run check` passes all 13 tests and the deterministic generated-file check.
- The regression parses actual key SVG XML, requires an SVG root and rejects descendant SVG elements, including namespace-prefixed forms.
- An in-memory regression probe reintroduced nested SVG markup and confirmed that the test fails. No invalid source or package was retained.
- A fresh build matches all six updated handoff packages byte for byte. The three fixed Stream Deck hashes are recorded below.
- Independent archive review checks all 257 Deck key images and 262 Ring icon templates, hashes, ZIP integrity, safe paths, image references, manual text submission and license bytes. All fixed Deck images have zero descendant SVG elements.
- Comparison with freshly extracted immutable baseline source verifies unchanged prompt text, action labels, identifiers, shortcuts, timing and navigation. Visual metadata and the explicit artwork attribution replacements are recorded separately.
- The Microsoft MIT artwork notice and retained legacy Lucide ISC notice remain intact. Alpha.3 packages include the original Microsoft MIT license for the artwork they actually contain; alpha.2's original ISC artwork notices are unchanged.

| Fixed Stream Deck package | SHA-256 |
| --- | --- |
| `ai-workflow-0.1.0-alpha.3.streamDeckProfile` | `f2699c2927ad246d2e05d567d3dc64f2cf19a99652d8a8f08a96e821f29384f1` |
| `browser-workflow-0.1.0-alpha.3.streamDeckProfile` | `7dcd16b33975fba221ece9c12c79def308fc74ad1f19717d0a3fe071dac16971` |
| `code-workflow-0.1.0-alpha.3.streamDeckProfile` | `867e23cf7a1690ee2568bc70ab03411d39d1fe86e208d34d0f21810a0da4110d` |

The published alpha.2 release was reverified anonymously: its nine assets match GitHub's SHA-256 digests, and all six packages match the published checksum file. Static inspection also finds nested SVGs in all 257 alpha.2 Deck key images. This identifies the same structural compatibility risk; alpha.2 was not freshly imported to reproduce the symptom. Alpha.2 remains unchanged; the corrected packages are distributed separately as alpha.3.

## Follow-ups kept separate

The MINI agent also reported a duplicate Default-page warning and tight title spacing. The fix preserves both existing page metadata and title geometry so its known package hashes remain reproducible. Neither observation was silently changed during source integration. Keep the candidate labeled Windows alpha and complete native actions, navigation, Ring import and hardware acceptance before claiming them tested.
