#!/bin/sh
set -eu
cd "$(dirname "$0")"
[ -f ../LegoQuest/app/src/main/assets/index.html ] || { echo 'Missing shared assets: keep LegoQuest next to BrickLog-Python.' >&2; exit 1; }
if [ ! -x .venv/bin/python ]; then
  if [ "$(uname -s)" = Linux ] && [ -x /usr/bin/python3 ]; then /usr/bin/python3 -m venv --system-site-packages .venv
  else python3 -m venv --system-site-packages .venv; fi
fi
.venv/bin/python -m pip install -r requirements-build.txt
if [ "$(uname -s)" = Linux ]; then
  .venv/bin/python -c 'import gi; gi.require_version("Gtk", "3.0"); gi.require_version("WebKit2", "4.1"); from gi.repository import Gtk, WebKit2' || {
    echo 'Install the Python GI bindings, GTK 3 and WebKitGTK 4.1 for your distro; see README.md.' >&2; exit 1; }
fi
.venv/bin/python -m PyInstaller --clean --noconfirm bricklog.spec
mkdir -p release-output
case "$(uname -s)" in
  Darwin) ditto -c -k --sequesterRsrc --keepParent dist/BrickLog.app release-output/BrickLog-macOS.zip
          echo 'Created release-output/BrickLog-macOS.zip (unsigned).';;
  Linux) tar -czf release-output/BrickLog-Linux.tar.gz -C dist BrickLog
         echo 'Created release-output/BrickLog-Linux.tar.gz. Keep its extracted folder together.';;
  *) echo 'Unsupported platform; the output is in dist/.' >&2; exit 1;;
esac
