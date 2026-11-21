# Build from this directory with: python -m PyInstaller bricklog.spec
import os
import sys

icon = 'icon.ico' if sys.platform == 'win32' else ('icon.icns' if sys.platform == 'darwin' else 'icon.png')
a = Analysis(['main.py'], pathex=[], binaries=[], datas=[(os.path.join(SPECPATH, '..', 'LegoQuest', 'app', 'src', 'main', 'assets'), 'assets'), ('icon.png', '.'), ('icon.ico', '.')], hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='BrickLog', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False, icon=icon)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name='BrickLog')
if sys.platform == 'darwin':
    app = BUNDLE(coll, name='BrickLog.app', icon=icon, bundle_identifier='com.bricklog.desktop')
