# Security and privacy

BrickLog is a personal project, not a security-certified application. No software is completely secure; this version has not received an independent security audit or been tested on every device. Keep your operating system, WebView, browser, Python and build tools up to date, and use a device account protected by a password.

## Protections in this version

- There are no cloud accounts or cloud sync. Previous versions' locally stored cloud configuration and session values are removed on startup; existing local progress is not intentionally removed.
- Desktop's asset server binds to `127.0.0.1` only and validates the host and allowed asset paths. It rejects framing and avoids MIME sniffing. It is not an authenticated service and cannot protect against a malicious local user or process.
- Android's WebView disables direct file access and mixed content, only navigates to the app's local HTTPS origin internally, and opens HTTP(S) external links through Android. Its native backup bridge limits export size. Content URI access remains enabled for Android's file picker.
- The shared UI escapes displayed text, checks external links and image URL schemes, and uses a Content Security Policy (CSP) that restricts resources and only permits the two bundled inline scripts by hash. Inline event handlers were removed. The policy permits `unsafe-eval` for pywebview's bridge and inline styles for the existing UI; it is defense in depth, not a guarantee against all injection.
- Backup import caps file size at 20 MiB, validates known structures, types, limits, URL schemes and dangerous property names, and asks before replacement. Do not import untrusted backups. Validation is not a guarantee that a file is safe or that every historical backup format is compatible.
- The Gradle wrapper checks its distribution checksum. The repository `.gitignore` excludes common secrets and generated outputs, but you must review staged files yourself.

## Residual risks and data

- Progress and notes are stored locally without app-level encryption, and JSON backups are **unencrypted**. Anyone with sufficient access to the device or a backup may read them. File-system protections and disk encryption depend on your device and configuration. Back up regularly and store backup files privately.
- Import **replaces**, rather than merges, the destination catalogue and progress. Export and verify a backup of the destination first. Clearing storage or uninstalling can delete data.
- Wikipedia refresh runs when the app starts and when requested. Online artwork and Google Fonts may be requested from third parties, and external links open external services; these services can observe your IP address and other request information. Game links may use HTTP, in which case the external website connection is not encrypted. Custom cover URLs also contact their host. Avoid loading private or sensitive URLs.
- Network-fetched catalogue data, third-party services, your operating system, WebView and installed Python/Gradle dependencies remain potential attack surfaces. Links can lead to phishing or harmful sites; review the destination before using them. The CSP deliberately limits `connect-src` to Wikipedia, but HTTPS images can come from external hosts to retain cover functionality.
- Desktop builds are unsigned and macOS builds are not notarized. Android's debug signing key is for testing, not a production identity; a release key should be kept private and reused for updates. Signatures do not guarantee that software is safe.
- If you used the removed cloud feature, deleting local credentials does not delete any data or accounts already stored on a Supabase project. Manage or delete that data directly in Supabase if desired.

## Maintaining the CSP

After editing either inline script in `LegoQuest/app/src/main/assets/index.html`, run `python3 tools/update_csp.py` from the repository root. The script recomputes the SHA-256 hashes in the CSP; without doing this, browsers/WebViews will block the modified scripts. Review policy changes rather than weakening it merely to make a test pass.
