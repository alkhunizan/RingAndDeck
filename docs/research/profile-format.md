# Profile formats and provenance

Prepared 2026-09-24 from six populated installed workflows. Public catalogs are the source of truth; no private extraction script is needed to rebuild. Installed originals were read only. New UUID namespaces replace profile, page, macro and action identities.

## Stream Deck

Inspected Stream Deck version: 7.5.1.22901. Roots use format `3.0`, model `20GBA9901` and a `Pages` object. The public root has no application binding or device serial/UUID. Current, Default and the top-level page list reference the populated Home page.

Native action UUIDs are Text, Open Child, Back to Parent, Website and Hotkey. Text settings disable Enter and typing mode. Folder/image references must resolve. Browser native shortcuts preserve the inspected action shape for Ctrl+Shift+A, Ctrl+Shift+T and Ctrl+0. Custom full-page capture and personal panel shortcuts were omitted.

[Elgato's manifest reference](https://docs.elgato.com/streamdeck/sdk/references/manifest/) describes packaged profiles and SVG image support. It primarily defines plugin manifests, not a complete standalone export schema. Native app import is still required for acceptance.

## Logitech Actions Ring

The inspected `Loupedeck72` profiles contain `ProfileInfo.json`, application metadata, folder/workspace layouts, macros, profile actions, image files and editable icon templates. The exported `.lp5` is a ZIP with these entries at its root.

The public edition uses the general `@_defaultwin` System context with no executable path. Folder action IDs match their target page IDs. Text macros have exactly a 1000 ms sleep followed by a SendText editor command, using the clipboard and no Enter action. Seven allowlisted standard Windows shortcuts are retained in Flow Ring. Local AI shortcut behavior becomes an equivalent editable prompt; two personal app launchers become Start AI Work and Quick Note prompts.

The installed `Loupedeck.Service.ApplicationProfile.LoadFromJson` accepts all three candidate profile JSON documents. A controlled probe identified that `supportedOs: Windows` is invalid; the native enum is `Win`. The native keyboard parser resolves all seven Flow Ring keys and modifiers. These checks do not write live configuration, import profiles or press physical controls.

Subsequent UI import checks found two constraints not enforced by that JSON loader: the layout mode must match the application's declared `System` mode, and Home exposes only 8 controls. Category folders show 9 actions. The builder keeps additional Home categories under More workflows. The final Code Ring Home and More contents were inspected in the native editor; full nested runtime and physical-control acceptance remain open in [validation](../VALIDATION.md).

[Logitech's profile documentation](https://support.logi.com/hc/en-au/articles/25575505956119-Profiles-in-Logi-Options-MX-Creative-Console) confirms `.lp4`/`.lp5` import. [Actions Ring guidance](https://support.logi.com/hc/en-ca/articles/17844647906967-Actions-Ring) covers action and icon customization. Exact overlay geometry is controlled by Logi Options+; rendered documentation is an illustrative guide.

## Visual assets and privacy

The renderer uses locally included Lucide SVG drawings with their ISC license. Original framing, gradients, accents and composition are generated from catalogs. Stream Deck packages contain SVGs; Logitech packages contain PNGs and icon templates with the same PNG imagery. No inherited personal artwork is copied.

Public guides deliberately retain full prompt text so reviewers can inspect behavior. Personal source inventories, hashes and extraction records are ignored local audit files. Publishing requires scanning the exact public tree and unpacked release artifacts, not merely trusting the catalogs.
