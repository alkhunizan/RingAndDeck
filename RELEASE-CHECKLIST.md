# Public release checklist

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

## Prerelease publication

- [x] Two complete 1279 by 722 showcase PNGs prepared with captions identifying browser captures of designed layouts, not native app screenshots.
- [ ] Recheck the final six packages, hashes and privacy scan after the layout-mode fix.
- [ ] Publish to [alkhunizan/RingAndDeck](https://github.com/alkhunizan/RingAndDeck) with the release marked as a prerelease.
- [ ] Verify all six download links, source/tag, SHA256SUMS.txt and showcase images from GitHub.
- [ ] Run GitHub CI and record its result without treating a workflow upload as a passing run.

## Native and hardware acceptance still required

- [x] Re-import the final Code Ring and confirm Home shows 8 populated controls.
- [x] Open More workflows in the final Code Ring UI and confirm Env & Tooling and Correct & Recover are present.
- [x] Record the earlier Plan & Scope folder rendering with its 9 unchanged actions, separately from final-build evidence.
- [ ] Verify deeper nested folders at runtime, text insertion and physical controls.
- [ ] Import all six candidates as separate profiles and verify native icons and navigation.
- [ ] Test representative text keys in scratch documents and actual AI composers without submitting.
- [ ] Test documented Windows/browser controls on the intended devices.
- [ ] Record device models, vendor versions and platforms used for acceptance.

Stream Deck opens but has not accepted the attempted UI input, so its import remains unverified. Publishing an alpha candidate does not complete the native or hardware acceptance checklist.
