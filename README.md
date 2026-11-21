# BrickLog

BrickLog is an **unofficial** LEGO video-game collection tracker for Android and desktop. Track played status, completion percentage, notes and platforms; browse covers and descriptions; filter the catalogue; add games; and export or import JSON backups. The catalogue starts from [Wikipedia's list of Lego video games](https://en.wikipedia.org/wiki/List_of_Lego_video_games), with additional entries. It may be incomplete or contain inaccurate data. Store links are searches, not guarantees that a game is available.

The desktop app uses Python and pywebview; **Node.js is not required**. Android and desktop share the interface and catalogue assets. Progress is stored on each device; transfer it manually with a JSON backup.

> **Before publishing to GitHub:** this project includes third-party game artwork and a brick icon. Some may be copyrighted or subject to non-free-use restrictions, and permission to redistribute has not been verified. Obtain the necessary rights or remove/replace those assets before making the repository public. LEGO is a trademark of the LEGO Group; this project is not affiliated with or endorsed by it. See [Artwork and licensing](#artwork-and-licensing).

## Repository layout

```text
BrickLog-Python/  Python desktop app, icons, launch/build scripts
LegoQuest/        Android app, Gradle wrapper, shared UI and catalogue assets
START-HERE.txt    Quick build overview
```

Keep `BrickLog-Python` and `LegoQuest` together: desktop source and build scripts use `LegoQuest/app/src/main/assets`. A packaged desktop build includes its own assets and does not require the source folders. Run builds on the target OS and architecture; these scripts do not cross-compile for every platform.

## Get the code

Download and extract the project ZIP, or clone your repository once it exists:

```sh
git clone <repository-url>
cd <repository-folder>
```

The first build requires internet access to download build dependencies. No Android release keystore or Node.js installation is included or required for offline use.

## Build for Android

### Prerequisites

- Python 3.10 or newer. On Windows, install the Python launcher (`py`).
- **JDK 17 or JDK 21**. The included Gradle 8.9 does not run on Java 25; newer is not always compatible. Your default Java does not have to change—see [Using a separate JDK](#using-a-separate-jdk-without-changing-system-java).
- Android SDK Platform 35 and Android SDK Build Tools, installed using [Android Studio](https://developer.android.com/studio). The SDK location must be configured through Android Studio's project setup (`LegoQuest/local.properties`) or the `ANDROID_HOME` environment variable.
- Internet access for the first build. The included Gradle wrapper downloads Gradle 8.9 and verifies its distribution checksum.

### Run the build script

On Windows, open PowerShell in `LegoQuest` and run:

```powershell
.\build-android.bat
```

On macOS/Linux, open a terminal in `LegoQuest` and run:

```sh
chmod +x gradlew build-android.sh
./build-android.sh
```

Choose an option:

1. **Installable debug APK (default):** no signing setup. Android tooling automatically creates or reuses a debug signing key. Output: `LegoQuest/release-output/BrickLog-installable-debug.apk`. Suitable for personal testing, not Play Store distribution.
2. **Unsigned release APK:** no key needed, but **Android cannot install it until it is signed**. Output: `LegoQuest/release-output/BrickLog-unsigned-NOT-installable.apk`.
3. **Signed release APK:** use or create a private release keystore. Output: `LegoQuest/release-output/BrickLog-release.apk`. Back up the keystore and password privately; future updates need the same signing key. Never commit either to GitHub. The helper assumes the key and keystore passwords match.

Transfer an installable APK to your device and open it. Android may ask you to allow installation from the app you used to open the APK. Android 7.0 or newer is required. The Android activity accounts for system bars and display cutouts on Android 15 and newer. Publishing to Google Play has additional signing and Android App Bundle requirements; these scripts build APKs only.

**Back up before upgrading:** Android only updates an existing app if the package and signing key match. A debug APK built on another machine, or a release signed with a new key, may require uninstalling the old version. Export and verify your JSON backup before uninstalling, as uninstalling deletes local data.

### Using a separate JDK without changing system Java

If `java --version` shows Java 25, obtain a compatible JDK 21. For example, download the Windows x64 JDK ZIP from [Eclipse Temurin](https://adoptium.net/temurin/releases/?version=21), extract it, and confirm its folder contains `bin/java.exe`. If you have Android Studio, its bundled JDK may be compatible; check its version first—it may itself be Java 25.

From PowerShell in `LegoQuest`, run the build in a temporary child process, replacing the example path with the **actual extracted JDK folder**:

```powershell
& "C:\Tools\jdk-21\bin\java.exe" --version
cmd /c 'set "JAVA_HOME=C:\Tools\jdk-21" && call build-android.bat'
```

This sets `JAVA_HOME` only inside the child process for that build. It does not change your system or PowerShell Java configuration. Use the command again on later builds. On macOS/Linux, run `JAVA_HOME=/path/to/jdk-21 ./build-android.sh` to set it only for that command.

### Finding the Android SDK on Windows

If the build says **SDK location not found**, first check whether the default Android Studio SDK location exists in PowerShell:

```powershell
Test-Path "$env:LOCALAPPDATA\Android\Sdk"
```

If the result is `True`, and you have extracted JDK 21 to `C:\Tools\jdk-21`, run this from the `LegoQuest` folder:

```powershell
cmd /c 'set "JAVA_HOME=C:\Tools\jdk-21" && set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk" && call build-android.bat'
```

Choose option 1 for an installable debug APK. Both variables are set **only in that child process**; your system Java and environment settings remain unchanged. Use your actual JDK path if different.

If the check returns `False`, open Android Studio → **Settings → Languages & Frameworks → Android SDK** to find the SDK location or install it. Check that **Android SDK Platform 35** and the SDK Build Tools are installed. Then use its actual path in the same command—for example, replace `%LOCALAPPDATA%\Android\Sdk` with `D:\Android\Sdk`. Android Studio can alternatively configure the ignored `LegoQuest/local.properties` file when the project is opened.

### Android troubleshooting

- **`Unsupported class file major version 69`:** Gradle is running on Java 25. Use JDK 17 or 21 as above. Verify the executable under your chosen `JAVA_HOME` with `--version`.
- **SDK location not found:** open `LegoQuest` in Android Studio and install/configure the SDK, or set `ANDROID_HOME` to the SDK directory. A common Windows location is `$env:LOCALAPPDATA\Android\Sdk`, if that's where Android Studio installed it.
- **App not installed / update rejected:** check APK signing key compatibility. Back up before removing any installed copy.
- An unsigned APK is not installable; choose option 1 if you want an installable APK without setting up a release keystore.

## Build for desktop

Install [Python](https://www.python.org/downloads/) 3.10 or newer and pip. Build on the target OS/architecture. No desktop build needs Java or Node.js.

### Windows

Install the Python launcher and [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) if it isn't already present. In `BrickLog-Python`, double-click `build-windows.bat`, or run:

```powershell
cd BrickLog-Python
.\build-windows.bat
```

The script creates `BrickLog-Python/release-output/BrickLog-Windows.zip`. Extract the entire archive and run `BrickLog/BrickLog.exe`; keep its supporting files beside it. It is unsigned, so Windows may warn. To run from source instead, use `run-windows.bat`. If an older copy fails with a Windows icon error, update both `BrickLog-Python/main.py` and `BrickLog-Python/icon.ico` from this version; Windows needs the ICO file for the window icon.

### macOS

On a Mac with Python and pip installed:

```sh
cd BrickLog-Python
chmod +x build-desktop.sh
./build-desktop.sh
```

Extract `release-output/BrickLog-macOS.zip` to obtain `BrickLog.app`. It is unsigned and not notarized; macOS may warn or block it. Public distribution requires appropriate Apple signing/notarization. To run from source use `./run-desktop.sh`.

### Linux

Install Python, venv/pip, PyGObject, GTK 3 and WebKitGTK 4.1. On Debian/Ubuntu, package names commonly include `python3-venv`, `python3-pip`, `python3-gi`, `gir1.2-gtk-3.0` and `gir1.2-webkit2-4.1`; availability varies by distribution. See the [pywebview installation guide](https://pywebview.flowrl.com/guide/installation).

```sh
cd BrickLog-Python
chmod +x build-desktop.sh
./build-desktop.sh
```

Extract `release-output/BrickLog-Linux.tar.gz`, keep the entire `BrickLog` folder, and run its `BrickLog` executable. Compatible GTK/WebKit runtime libraries are still required on the target machine. Build on a compatible distribution and architecture. To run from source use `./run-desktop.sh`. If the build cannot find GI bindings, ensure they are installed for the distribution Python; delete an existing `BrickLog-Python/.venv` created with a different Python and retry.

Desktop build scripts create a virtual environment and install the pinned dependencies. The packaged desktop apps do not need Python on the destination computer. The desktop GUI and packages have not been tested on every platform or device. See [desktop details](BrickLog-Python/README.md).

## Backups and local data

Use the app's JSON export/import feature and verify backups regularly. To transfer progress from Android to desktop, export on Android, copy the JSON file to the computer, then import it on desktop. Import replaces the destination's current catalogue and progress, so back up the destination first. The app does not provide online account sync. Local data can be lost when app storage is cleared or the app is uninstalled. Desktop uses a local-only server on `127.0.0.1:18765`; its port must remain stable for the local storage origin. If the port is in use, close the other process or another copy of BrickLog.

## Security and privacy

BrickLog uses local storage and unencrypted JSON backups. Online catalogue refresh, fonts, images and external links still contact third parties. The app includes URL checks, a content security policy, limited desktop asset serving and stricter backup validation. Read [SECURITY.md](SECURITY.md) for the protections, residual risks and safe-use guidance.

## Artwork and licensing

The catalogue draws on Wikipedia and other sources, which have their own licensing and attribution requirements. Bundled game images may be copyrighted, non-free, screenshots or icons rather than official covers; image source links appear in game details. The brick icon is a cropped/resized image from [Brick Owl](https://www.brickowl.com/catalog/lego-dark-purple-brick-2-x-2-3003); its reuse license has not been verified. No blanket license for third-party assets is granted here. Review permissions and attribution before uploading the repository publicly or distributing builds. No open-source license for the project code has been selected; the owner should choose one only after reviewing rights to all included material.

## Publishing your own GitHub repository

1. Review the artwork and licensing section above and remove or replace anything you don't have permission to publish.
2. Create a new repository on GitHub. In a terminal at the project root, initialize Git if needed, review `git status`, then add and commit the files. Add your own remote and push using GitHub's instructions.
3. The included `.gitignore` excludes build output, virtual environments, local Android SDK configuration, APKs, archives, keystores and common secret files. It is a safeguard, **not a substitute for reviewing staged files** with `git status` and `git diff --cached`. Never commit keystores, passwords, private credentials, backups or session tokens. If a secret was already committed, ignoring the file does not remove it from history; rotate it and clean the history before sharing.
