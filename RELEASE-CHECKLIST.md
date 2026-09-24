# Public release checklist

Current alpha prerelease: `v0.1.0-alpha.3`. It adds colorful artwork and the MINI-reported Stream Deck nested-SVG fix while preserving action behavior. Public `v0.1.0-alpha.2` remains unchanged. The owner authorized GitHub alpha.3 publication on 2026-09-24. Marketplace submissions remain separate.

## Alpha.3 local preparation

- [x] Import the complete colorful handoff source, including the MINI fix, into an isolated Git branch.
- [x] Preserve all six updated handoff package hashes in a fresh local build.
- [x] Pass all 13 tests and deterministic output checks; parse key XML to reject descendant SVG elements.
- [x] Independently inspect 257 Deck key images and 262 Ring icon templates, archive integrity, references and license bytes.
- [x] Compare native behavior with immutable public main `bf98287c53d034540ba4204ba4d220ffc9dc114c`.
- [x] Record the MINI-reported Home rendering and remaining native limits separately in [the fix note](docs/STREAM-DECK-ICON-FIX.md).
- [x] Prepare [draft alpha.3 release notes](docs/releases/v0.1.0-alpha.3.md).
- [ ] Complete native action, folder/Back, Ring import and physical-device acceptance.
- [x] Obtain the owner's explicit approval for GitHub alpha.3 publication. Marketplace submissions remain separate.
- [x] Rebuild and match all six prepared alpha.3 package checksums before publication; preserve alpha.2.

The following sections retain historical alpha.1/alpha.2 preparation evidence.

## Preparation completed

- [x] Three Actions Ring and three Stream Deck source catalogs and native candidate packages prepared.
- [x] Full prompt/action guides and 55 generated layout previews prepared.
- [x] Shared visual theme and meaningful action icons included in native exports.
- [x] No AI API client, embedded credential, private app binding or custom executable action.
- [x] Personal names, clients, accounts, paths and inherited identifiers removed from profile content.
- [x] Text actions require manual submission; standard Windows/browser shortcuts are documented.
- [x] Fresh project identifiers and MIT/ISC notices included in packages.
- [x] All 13 unit tests pass, including declared ring layout modes, Home capacity and folder references.
- [x] Ring Home uses 8 controls and folders at most 9; More workflows preserves all 81 prompts in both Code Ring and Work Ring.
- [x] Artifact references, archive integrity and deterministic local rebuild checks recorded in [validation](docs/VALIDATION.md).
- [x] Native Logitech loader accepts all three ring profile JSON documents; seven keys parse correctly.
- [x] Independent review findings corrected and re-reviewed.
- [x] Rendered page bounds and all six Home layouts checked.
- [x] Exact public source and unpacked candidate artifacts scanned for secrets and personal references.
- [x] All 900 original source files verified unchanged by SHA-256 comparison.
- [x] Original installed profiles backed up before candidate import work.
- [x] Owner authorized the public GitHub repository and `v0.1.0-alpha.1` prerelease.

## Alpha.2 build and publication

- [x] Update Sharp from 0.34.5 to 0.35.4; npm audit now reports 0 vulnerabilities, down from 2 high-severity advisories.
- [x] Confirm all six packages remain byte-identical after the dependency upgrade with the release version held constant.
- [x] Pass all 13 unit tests after the build dependency update.
- [x] Verify final alpha.2 package contents, hashes and privacy scans after the version bump.
- [x] Publish `v0.1.0-alpha.2` as a prerelease with six packages, checksums and showcase images.
- [x] Download all 9 alpha.2 assets anonymously and compare hashes.
- [x] Record passing Windows and Ubuntu CI runs for alpha.2, including the dependency audit.

## Prior alpha.1 publication verified

- [x] Two complete 1279 by 722 showcase PNGs prepared with captions identifying browser captures of designed layouts, not native app screenshots.
- [x] Recheck the final six packages, hashes and privacy scan after the layout-mode and Home-capacity fixes.
- [x] Publish to [alkhunizan/RingAndDeck](https://github.com/alkhunizan/RingAndDeck) with the release marked as a prerelease.
- [x] Download all 9 release assets anonymously and compare hashes; verify all four repository screenshots byte for byte.
- [x] Verify passing GitHub CI on Ubuntu and Windows for both main and the release tag; links are in the validation record.

## Native and hardware acceptance still required

The checked UI steps below belong to alpha.1. Alpha.2 retains the same actions and artwork; a separate alpha.2 import has not been verified.

- [x] Re-import the final alpha.1 Code Ring and confirm Home shows 8 populated controls.
- [x] Open More workflows in the final alpha.1 Code Ring UI and confirm Env & Tooling and Correct & Recover are present.
- [x] Record the earlier Plan & Scope folder rendering with its 9 unchanged actions, separately from final-build evidence.
- [ ] Verify deeper nested folders at runtime, text insertion and physical controls.
- [ ] Import all six candidates as separate profiles and verify native icons and navigation.
- [ ] Test representative text keys in scratch documents and actual AI composers without submitting.
- [ ] Test documented Windows/browser controls on the intended devices.
- [ ] Record device models, vendor versions and platforms used for acceptance.

The historical Stream Deck attempt did not establish an import. The separate alpha.3 MINI report now establishes reported Home rendering for all three fixed profiles only. Publishing an alpha candidate does not complete the native or hardware acceptance checklist.
