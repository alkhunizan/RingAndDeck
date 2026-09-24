# Six-profile public edition

Goal: prepare three existing Logitech Actions Ring workflows and three existing Stream Deck workflows, remove personal information and dependencies, and substantially improve the visual design. The initial preparation scope excluded publication; the owner subsequently authorized the public GitHub repository and alpha release. Existing installed source profiles remain preserved.

## Selected workflows

Selection uses the installed local profiles, not online rankings. Criteria: depth of useful workflows, distinct purpose, ability to generalize, and existing populated structure.

| Device | Public edition | Source workflow | Reason |
| --- | --- | --- | --- |
| Actions Ring | Code Ring | Coding Ring v3 | Complete 81-prompt development lifecycle |
| Actions Ring | Work Ring | Business assistant ring | 81 prompts spanning clients, team, focus, writing, operations and recovery |
| Actions Ring | Flow Ring | Visual AI productivity ring | AI follow-ups plus practical Windows controls across eight folders |
| Stream Deck | Code Workflow | VS Code | Complete coding workflow, reusable across coding assistants |
| Stream Deck | AI Workflow | Agent Cockpit | General AI work with focus, decisions and context |
| Stream Deck | Browser Workflow | Browser Cockpit | Evidence-based browser analysis, reporting, focus and public service shortcuts |

Duplicate variants with private window-layout hotkeys were not selected. Personal business bookmarks become generic public service entry points or are omitted where they have no portable meaning. Proprietary local AI hotkeys become self-contained prompts with explicit manual submission. Standard Windows controls remain functional shortcuts.

## Visual direction

The alpha.3 candidate uses vivid, full-color Microsoft Fluent Emoji Flat illustrations on clean pale fields. A navy title strip keeps Stream Deck labels readable, with shared native and preview sizing from 8 to 10. Familiar objects connect directly to action meanings: magnifiers for search and review, pens for writing, tools for building, a lady beetle for debugging, a robot for AI, a calendar for scheduling, a stopwatch for focus, and a shield or key for security. Semantic accents, folder cues and consistent Back controls help navigation across devices.

Exported icons and documentation previews share the same artwork. Illustrations retain their upstream colors and Microsoft MIT license, with pinned provenance and hashes in `assets/color-icons/`. Earlier Lucide assets retain their ISC license; original composition and code use the project MIT license. This colorful direction follows the owner's rejection of the earlier warm revision.

## Required evidence

- Exactly three native package candidates per device, with editable catalogs and full guides.
- Every action remains useful or has a documented portable replacement. No dead personal shortcut.
- No personal accounts, client names, device identities, local executable paths or secret values.
- Native package structures, references, icons and text settings validated; deterministic builds and exact release hashes.
- Render every page and review small-size readability, clipping and navigation.
- Confirm source files remain unchanged against the private pre-edit hash baselines.
- Record application import and physical-control testing separately. Do not treat generated previews as hardware screenshots.

## Current progress

The original two Stream Deck candidates are preserved in an ignored private baseline archive. Published alpha.2 contains six packages and 55 layout guides; its publication and limited native Code Ring evidence are recorded in [VALIDATION.md](VALIDATION.md). The colorful alpha.3 artwork is included in the alpha.3 prerelease. Fresh validation passes 13 automated tests, deterministic output, package/action comparisons, all 55 rendered guides and 1,269 companion website tests. Full interactive device acceptance remains open.
