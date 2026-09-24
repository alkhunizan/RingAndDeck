# Setup and first-use check

Build with the README commands. Check downloaded files against `SHA256SUMS.txt`. Back up existing profiles before any import and retain the backups.

## Stream Deck

In Stream Deck profile preferences, use the import control for each `.streamDeckProfile` file. Keep **Code Workflow**, **AI Workflow** and **Browser Workflow** as separate new profiles. Do not overwrite a personal profile. No executable binding is supplied.

The target is a Windows 15-key grid. XL, Mini, Plus, mobile and macOS conversion have not been tested.

1. Confirm each Home page has 15 labeled keys, all icons load and folders open.
2. Open every folder and use Back to return.
3. Focus a blank scratch text document. Try Write Goal, Orient Me and a browser-analysis prompt. Confirm the common scope guard and matching guide text appear without an extra Enter.
4. In Browser Workflow, test the public website buttons and check which browser/account opens. Links use the default browser, not a named personal profile.
5. In a disposable Chrome or Edge window, verify Tab Search (`Ctrl+Shift+A`), Reopen Tab (`Ctrl+Shift+T`) and Zoom Reset (`Ctrl+0`). Other browsers may use different shortcuts.
6. Try a prompt in an empty AI composer without sending it. Replace placeholders, review the full text and submit only when ready.

## Logitech Actions Ring

Open Actions Ring customization in Logi Options+. Use the profile import control to select each `.lp5` file. Keep **Code Ring**, **Work Ring** and **Flow Ring** as separate profiles. The packages use the general System profile context; assign them to a preferred application yourself if desired.

The native target is `Loupedeck72`, matching the inspected Actions Ring installation. A supported Logitech device and Logi Options+ are required. The native JSON loader was tested; interactive import remains an acceptance step.

1. Verify the Home folder counts: Code 9, Work 9, Flow 8.
2. Open every folder. Each contains 9 actions. Test the application's own return/back navigation.
3. Focus a blank scratch document before invoking text. Wait for the one-second overlay delay and confirm the full prompt is pasted without Enter.
4. Review the default clipboard behavior. Text macros explicitly use the clipboard to preserve multiline content.
5. Test the seven Flow Ring Windows controls separately, only when you intend their effects: Dictate (`Win+H`), Capture (`Win+Shift+S`), Clipboard (`Win+V`), Plain Paste (`Ctrl+Shift+V`), Files (`Win+E`), Task View (`Win+Tab`) and Snap Layout (`Win+Z`).
6. Plain Paste requires support in the focused app. Dictation and clipboard history require the relevant Windows features to be configured by you. Snap Layout requires a supported Windows version. No custom AI hotkey or paid plugin is required.
7. Test text in an empty AI composer without sending. Do not test text macros in terminals or address bars.

Logitech's [profile documentation](https://support.logi.com/hc/en-au/articles/25575505956119-Profiles-in-Logi-Options-MX-Creative-Console) describes `.lp4`/`.lp5` import. Menu names may vary by release.

## Editing and troubleshooting

- Stream Deck catalogs use `column,row` positions; child slot `0,0` is reserved for Back. Ring catalogs use ordered folders and actions, up to 9 per level.
- Text prompts often need `[TASK]`, `[LANGUAGE / TONE]`, `[TIME ZONE]` or other context supplied after pasting. No private account is preconfigured.
- Wrong input receives text: focus the intended input before activation. Stop if a host treats multiline paste as submission.
- Missing icons or a rejected import: record the vendor version and exact error, keep the original profile, and compare hashes. Do not overwrite a working setup to troubleshoot.
- No API key field: expected. Configure credentials in the AI app's own supported UI, never inside a shared profile action.
- Re-importing may create duplicate profiles. Inspect what the vendor app imported before removing an older version.
- A prompt expects an unavailable tool: supply the context yourself or use the manual/draft fallback. Profiles do not install connectors or grant access.
