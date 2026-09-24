# Privacy and security

The six profile packages contain prompts, icons, navigation, public website links and a small set of documented keyboard shortcuts. They contain no AI API client, helper server, telemetry or stored credentials. The builder needs no service authentication.

## Storage and transmission

Source catalogs are plain JSON. Both export formats are readable ZIP archives, not encrypted vaults. After import, the vendor app stores prompt text and settings locally. Typical inspected Windows locations are `%APPDATA%/Elgato/StreamDeck/ProfilesV3` and `%LOCALAPPDATA%/Logi/LogiPluginService/Applications/Loupedeck72`.

Text actions paste into the focused input and do not press Enter. Clipboard contents may be replaced. The AI provider receives the composer content only when you submit it or its own app behavior sends it. Your chosen app controls credentials, connected tools, retention and charges; the profiles do not change those settings.

Website buttons open public URLs through the default browser, which may already be signed into an account. They do not select an account for you. Windows shortcut buttons invoke operating-system or application features, which have their own privacy and network behavior. Dictation may process speech through Windows services according to your settings.

## Scope and approval

Every AI prompt receives a common guard covering authorized scope, unavailable tools, secrets and consequential actions. That is guidance to the assistant, not a security boundary. Check the app's real permissions and review actions before approving them.

The account-access prompt helps find a sign-in or recovery route and a vault entry name. It never requests password, token or recovery-code values. Work prompts draft messages, tasks and scheduling previews instead of assuming access to the author's services.

## Before sharing a customization

1. Review every prompt, setting, link and image for personal or client information.
2. Keep secrets, private account URLs, device identifiers and local executable paths out of catalogs and exports.
3. Run the tests, build and generated-output check. Unpack the exact release packages for inspection and secret scanning.
4. Pattern-based scans have limits. A custom domain, prose or image can disclose information without matching a credential pattern.
5. If a secret was published, rotate or revoke it. Editing the latest file does not remove previous downloads or Git history.

Do not put secret values or private exports in a public issue. Use a synthetic reproduction. If a future repository enables private vulnerability reporting, use its Security tab; otherwise ask for a private reporting route without sending the sensitive material.
