# Contributing

Improve an existing workflow before adding another page. Keep prompts provider-neutral, focused and useful with a clear manual fallback when tools are missing.

1. Edit `profiles/*.json` for Stream Deck or `rings/*.json` for Actions Ring. Packaging lives in `scripts/build.py` and `scripts/ring.py`; shared visuals live in `scripts/artwork.py`.
2. Keep labels readable on a 15-key device. Use one or two lines, at most 12 characters per line.
3. Preserve manual submission of text prompts. Do not add secrets, account-specific links, personal paths, arbitrary scripts or auto-send. Native keyboard actions must be allowlisted and documented. Website actions require public HTTPS hostnames without credentials or account parameters.
4. Use original or compatibly licensed artwork. Preserve the Microsoft Fluent Emoji MIT attribution and any retained Lucide ISC notices in exports. Do not copy paid icon packs or provider logos into the repository.
5. Run `npm ci`, the build, unit tests and generated-output check from the README. Inspect all six Home layouts and every changed folder.
6. Describe the problem solved, the resulting behavior and the exact validation performed. Say plainly if application import or physical buttons were not tested.

Use synthetic examples in issues and pull requests. The generated docs and previews are committed; `dist/` is generated for release assets. Private user profiles and local audit files must stay outside public history.

Commit `.generated-files.json` with the generated guides and previews. It records the builder's outputs so removed catalogs and renamed versions cannot silently leave old content behind. If a build reports stale files, review and archive the exact listed files outside the repository, then rebuild. Do not bypass this check by editing the inventory.
