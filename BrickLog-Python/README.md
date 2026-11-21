# BrickLog desktop — Python edition

This is the same interface as the Android app. No Node.js is required. It uses Python and pywebview, which displays the app in the operating system's web view. Local progress is stored by that web view. Use JSON export/import to transfer progress between devices.

## Windows: run from source

1. Install Python 3.10 or newer from https://www.python.org/downloads/. During installation select **Add Python to PATH**. Windows also needs Microsoft Edge WebView2 Runtime; it is installed on most recent Windows systems. If needed, download it from Microsoft.
2. Extract the ZIP. Open a terminal in the `BrickLog-Python` folder (in File Explorer, open the folder, type `cmd` in the address bar and press Enter).
3. Run:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

For later runs, open the same folder and run the last two commands again. Internet is needed for the initial installation.

## macOS and Linux: run from source

Install Python 3.10+ and pip, then in a terminal:

```sh
cd /path/to/BrickLog-Python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

On Linux, pywebview requires a GTK/WebKit backend and system packages (including PyGObject and WebKitGTK); the exact packages differ between distributions. See https://pywebview.flowrl.com/guide/installation for current backend instructions. On macOS, pywebview uses the system WebKit backend. The GUI environment must support a graphical desktop.

## Create a standalone app (optional)

Build on each target operating system. With the virtual environment activated:

```sh
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm bricklog.spec
```

Find the packaged app in `dist/BrickLog` (on macOS an app bundle may also be generated). It is unsigned; operating systems may warn before launching. Platform dependencies such as WebView2 or Linux WebKitGTK can still be required. The packaged builds have not been tested on all operating systems.

## Data and backups

The app starts a local server on `127.0.0.1:18765`; it is not exposed to your network. Keep the port fixed to preserve the browser storage origin. If another process uses it, quit that process or the other BrickLog instance. Local WebView storage persists across restarts but may be lost if app/browser data is cleared; export JSON backups regularly and before upgrading. To transfer progress, export a JSON backup on the original device and import it on the destination; import replaces the destination data, so back it up first. This desktop Python edition has not been tested on each OS.

Switching from the earlier Electron desktop project: it uses a different storage origin. Export a JSON backup from the old version and import it into the Python version, using the export and import buttons. Back up before making changes.

## Convenience scripts

- Windows: double-click `run-windows.bat` to run from source; `build-windows.bat` builds `dist/BrickLog/BrickLog.exe`. Keep the entire generated folder, not just the .exe.
- macOS/Linux: run `./run-desktop.sh` to launch or `./build-desktop.sh` to build. If permissions are missing after extraction, run `chmod +x *.sh` first. macOS creates `dist/BrickLog.app`; Linux creates `dist/BrickLog/BrickLog` (keep the entire folder). Build on the target OS. Scripts create a local `.venv` and install dependencies with pip; they need Python, pip, internet, and the WebView system dependencies mentioned above.

On Linux, scripts create the virtual environment with `--system-site-packages` so the distro Python can see its installed `gi` bindings. Use the distribution Python with the corresponding GTK/WebKit packages; if you already created `.venv` without this option, remove it and rerun the script.

## Icon image
The launcher and in-app icon use a cropped/resized image of a dark-purple LEGO 2×2 brick (part 3003), from Brick Owl: https://www.brickowl.com/catalog/lego-dark-purple-brick-2-x-2-3003 and https://img.brickowl.com/files/image_cache/larger/lego-dark-purple-brick-2-x-2-3003-1764893.jpg. This is third-party imagery; no reuse license has been verified. Obtain permission before redistributing or publishing. LEGO is a trademark of the LEGO Group; BrickLog is unofficial.

The Android and desktop source projects share the catalogue and artwork in `../LegoQuest/app/src/main/assets`. Keep the `BrickLog-Python` and `LegoQuest` folders together when running or building from source. Desktop packaged builds include their own copy of those assets, so the packaged app does not need the source folders.

## Release archives
`build-windows.bat` creates `release-output/BrickLog-Windows.zip`; `build-desktop.sh` creates `release-output/BrickLog-macOS.zip` or `release-output/BrickLog-Linux.tar.gz`. Build each on the target OS and architecture. Archives include the executable and supporting files, so Python is not required on the destination machine. Windows needs WebView2 Runtime; Linux still needs GTK 3 and WebKitGTK 4.1 system libraries. Desktop outputs are unsigned; macOS builds are also not notarized, so system security warnings or blocks are expected. For public distribution, arrange appropriate signing and notarization separately. These outputs were not GUI-tested on Windows/macOS/Linux.

For Debian/Ubuntu-style Linux, typical build prerequisites include `python3-venv python3-pip python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.1`; package names and availability vary by distro. Build using the distro Python corresponding to those bindings. The build script validates the bindings and WebKit 4.1. If it reports missing bindings but they are installed, delete the local `.venv` and rerun it with the correct system Python available as `/usr/bin/python3`.
