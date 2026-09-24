# Known issues and limits

- Code Ring's alpha.1 native import, populated 8-control Home and More workflows folder have been checked. Alpha.2 has the same actions and artwork but has not been separately imported. Deeper nested runtime navigation, text pasting and physical-button behavior remain unverified. Work Ring and Flow Ring UI imports are still pending.
- Stream Deck opens but has not responded to the attempted UI input. No Stream Deck UI import is claimed. Original profiles are backed up; import candidates separately from working profiles.
- Logitech's native JSON loader accepted earlier ring files without detecting an invalid layout mode or proving the Home capacity. Parsing success is not UI or hardware acceptance.
- The showcase PNGs are browser captures of designed generated-layout pages, not native app or hardware screenshots. They do not establish that a profile imports or works on a device.
- Targets are Windows 15-key Stream Deck and Logitech Actions Ring in `Loupedeck72` format. Other layouts and macOS are untested.
- Text actions use the focused input, may replace the clipboard and can be handled differently by different apps. Test a scratch document first.
- Browser links open the default browser and its current account state. The profiles do not route to a specific browser profile or account.
- Windows features, plain-paste support and browser shortcuts depend on the receiving app and OS. No custom AI hotkey is required.
- Prompts cannot grant app access, make unavailable tools work or enforce their own approval instructions.
- Secret/portability scanners use patterns and manual review. They cannot guarantee detection of every sensitive fact or image.
- Builds are deterministic within the tested toolchain. Sharp raster output can vary across operating systems or native library versions; compare hashes produced by the same release build.
- Re-import behavior may create duplicates. Verify vendor app behavior before removing a prior version.

## Corrected during preparation

- Alpha.2 updates the Sharp build dependency from 0.34.5 to 0.35.4. The npm audit result changed from 2 high-severity advisories to 0 vulnerabilities. Before the release-version bump, all six generated packages remained byte-identical; profile functionality and artwork are unchanged.

- Replaced personal AI commands and machine hotkeys with self-contained prompts.
- Removed personal clients, account references, private URLs, executable bindings and inherited identifiers.
- Replaced password-retrieval instructions with account recovery and vault navigation guidance.
- Made planning actions stop before Git/worktree mutations; replaced automatic task creation and publishing with scoped drafts.
- Populated Stream Deck Home pages and added stale-artifact rejection.
- Corrected the Logitech OS enum from the rejected `Windows` value to the native `Win` value, confirmed through its installed loader.
- Corrected ring layout modes from `main` to the declared `System` value and added a Home-folder regression test. The final Code Ring re-import now shows a populated Home.
- Limited Actions Ring Home to 8 controls and folders to 9. Code Ring and Work Ring use More workflows, retaining all 81 prompts each. More workflows opens in the final Code Ring UI; deeper nested runtime behavior is still open above.
- Replaced reused category-only artwork with a shared theme and action-specific licensed symbols.
