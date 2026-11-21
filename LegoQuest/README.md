# BrickLog for Android

An unofficial LEGO video game collection tracker. Browse Wikipedia's List of Lego video games, save status, percentage, personal platform and notes locally, and see collection statistics. Search, filter by inferred franchise or platform, sort by title, progress, release year; select multiple games to edit status, progress and platform; expand descriptions and platform lists; add missing games manually; and export/import a JSON backup.

## Build and install
1. Install Android Studio with Android SDK 35 and an internet connection.
2. Open the `LegoQuest` folder as a project. Let Android Studio download Gradle and sync. (The Gradle 8.9 wrapper is included and downloads Gradle on first use.)
3. Run on an Android device/emulator (Android 7.0 or later), or use Build > Build APK(s).

A bundled snapshot of the Wikipedia list is available offline. Internet is needed to refresh the list and fetch descriptions and images. Cached catalogue entries and your progress are stored locally in the WebView; clearing app storage or uninstalling deletes them. Export a backup first. The catalogue is built from the main games table on the English Wikipedia List of Lego video games. Release years and platforms come from that table. Wikipedia can change its page structure, and its list may be incomplete. Descriptions and thumbnails are fetched from linked articles when available. Games without articles remain in the catalogue. Covers are Wikipedia thumbnails and may sometimes be missing or not be box art. Add missing titles manually. This is not an official LEGO app. Wikipedia content is subject to its licenses; see each article for attribution and licensing.

The HTML file can also be served over HTTP for a browser preview. Wikipedia's API and images require network access.

Release sorting uses the year published in the Wikipedia list (not an exact date). The franchise filter is inferred from game titles; unrecognized titles are grouped under Other. Wikipedia images are loaded online from article thumbnails, may not be box art, and may not exist for every title. A set of locally bundled thumbnail images is included so those covers display offline and do not depend on the image host. Other artwork still requires an internet connection.

The dark purple theme is built in. Additional verified mobile game artwork is linked from AppBrain/Google Play, Internet Archive, StrategyWiki, MobyGames, Brickipedia, APKPure and APKVision; open a game's details for the artwork source. You can paste a direct HTTPS image URL in the game details and save it as a custom cover; your choice remains in your backup and takes priority over default artwork. Some artwork is bundled locally; other artwork is loaded from third-party hosts and may disappear, be blocked, or require internet. Some titles have no verified cover. Artwork rights belong to their respective owners.

The included thumbnails are from Wikipedia and other credited sources and may be copyrighted or subject to non-free-use restrictions. This project is intended for personal use; obtain appropriate permissions before redistributing images or publishing the app. Image source links are in game details.

All retained games from the original Wikipedia snapshot have a locally bundled image. Some images are app icons, screenshots, gameplay video thumbnails, or images of the associated LEGO set rather than game covers; open game details for the source. Newly added or future Wikipedia entries may not have images.

## Expanded catalogue
The offline catalogue includes 40 additional standalone games (including browser and mobile games) from the Video Game Title Lists Wiki and the announced LEGO Skylines. This is a curated expansion, not a comprehensive list of every historical browser game. Skylines is unreleased; its 2027 year is the Nintendo Switch 2 listing, not a confirmed universal release date. Older games may be delisted or require obsolete browser technology. Separate editions and platform ports were not added. Existing Wikipedia entries, including its compilations and handheld titles, have not been removed so existing progress remains intact. Many additional games have no verified artwork yet; custom cover URLs can be used. Refresh merges the supplemental games with the Wikipedia list using normalized exact titles, preserving progress when a matching entry is added to Wikipedia. Backup before upgrading.

DUPLO games are excluded from the bundled catalogue, cached catalogues, restored backups and Wikipedia refreshes. Existing saved progress records are not deleted. Additional mobile app icons and browser game artwork are bundled, with source links in game details; some additional games still have no verified artwork.

LEGO Friends games are excluded alongside DUPLO games, including on refresh and backup import. Saved records are not deleted. All current bundled catalogue entries have a local image, including icons, screenshots and game menus where cover art is unavailable. Fixed the Android asset route for LEGO Skylines artwork. Future Wikipedia entries and user-added games may have no images.

Promotional discs from the Video Game Title Lists Wiki are excluded by exact normalized title on startup, refresh, and backup import. This does not remove separately released browser or downloadable games, including the three Exo-Force games. Existing progress records are not deleted.

## Platform links and browser games
The platform list in each game’s details includes store search links: Instant Gaming is first for PC and consoles, followed by Steam or an appropriate console store where applicable. Android and iOS link to their app stores; older systems also have a physical-copy search. These are searches, not verified product listings: check title, platform, region, edition and current availability before purchase. The eight bundled browser games include links to preserved versions or explicitly labelled fan remakes; compatibility and availability vary, especially on mobile. Browser game release years are sourced, with links in game details. Links require internet and open externally.

## Desktop app and backups
A matching desktop source project is included in the parent bundle under `BrickLog-Python`. Transfer progress between devices using JSON export and import. Import replaces the destination catalogue and progress, so export a backup there first. There is no account sync. The launcher icon is a purple 2×2 brick.

## Build an Android APK
Install Python 3.10+, JDK 17 or 21, Android SDK 35 and build tools. Set `ANDROID_HOME` or configure `local.properties` in Android Studio. Run `build-android.bat` on Windows or `./build-android.sh` on macOS/Linux. Gradle and dependencies download on first use. Choose:

1. **Installable debug APK** (default): no keystore setup is required. The Android tooling automatically creates or reuses a debug signing key. Output: `release-output/BrickLog-installable-debug.apk`. This is not intended for Play Store publication.
2. **Unsigned release APK**: no signing key is required, but Android will not install it until it is signed. Output: `release-output/BrickLog-unsigned-NOT-installable.apk`.
3. **Signed release APK**: use or create a personal release keystore. Output: `release-output/BrickLog-release.apk`. Keep the keystore and password backed up privately to sign future updates; never include them in shared archives. The script assumes the keystore and key passwords match. The menu also calls `build-release.py`, which can be run directly.

APK updates require the same application ID and signing key as the installed app. A debug key from another computer or a new release key may not match the installed app. Export and verify your JSON backup before uninstalling. Play Store publishing has separate signing and app bundle requirements; these scripts make APKs only.

Advanced: `./gradlew assembleRelease` produces an unsigned APK unless all four environment variables `BRICKLOG_KEYSTORE`, `BRICKLOG_STORE_PASSWORD`, `BRICKLOG_KEY_ALIAS` and `BRICKLOG_KEY_PASSWORD` are set. Never commit these values or the keystore.

### Windows SDK location and Java 25
If the Android SDK is not found, check `Test-Path "$env:LOCALAPPDATA\Android\Sdk"` in PowerShell. If true, and JDK 21 is extracted at `C:\Tools\jdk-21`, from this folder run:

```powershell
cmd /c 'set "JAVA_HOME=C:\Tools\jdk-21" && set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk" && call build-android.bat'
```

Both settings apply only to that child process. Substitute your actual paths. If the SDK directory does not exist, find or install it in Android Studio → Settings → Languages & Frameworks → Android SDK, including Android SDK Platform 35 and Build Tools. The root README has full details.

Android 15 and newer: the Android activity applies system-bar and display-cutout insets so the interface does not sit beneath the notification or navigation bars. Older Android versions use the system default layout.
