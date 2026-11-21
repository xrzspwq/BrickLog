#!/usr/bin/env python3
"""Choose an installable debug APK, an unsigned APK, or a signed release."""
from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    print('BrickLog Android build')
    print('1. Installable APK with automatic debug signature (no keystore setup)')
    print('2. Unsigned release APK (NOT installable until signed)')
    print('3. Signed release APK (requires a private release keystore)')
    choice = input('Choose 1, 2 or 3 [1]: ').strip() or '1'
    if choice == '3':
        subprocess.run([sys.executable, str(ROOT / 'build-release.py')], cwd=ROOT, check=True)
        return
    if choice not in ('1', '2'):
        raise ValueError('Choose 1, 2 or 3.')
    # Never accidentally sign an intended unsigned build with inherited credentials.
    env = os.environ.copy()
    for key in ('BRICKLOG_KEYSTORE', 'BRICKLOG_STORE_PASSWORD', 'BRICKLOG_KEY_ALIAS', 'BRICKLOG_KEY_PASSWORD'):
        env.pop(key, None)
    task = 'assembleDebug' if choice == '1' else 'assembleRelease'
    wrapper = ROOT / ('gradlew.bat' if os.name == 'nt' else 'gradlew')
    cmd = ['cmd', '/d', '/c', str(wrapper), '--no-daemon', task] if os.name == 'nt' else [str(wrapper), '--no-daemon', task]
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)
    source = ROOT / 'app' / 'build' / 'outputs' / 'apk' / ('debug' if choice == '1' else 'release') / ('app-debug.apk' if choice == '1' else 'app-release-unsigned.apk')
    if not source.is_file():
        raise RuntimeError(f'Expected output not found: {source}')
    out = ROOT / 'release-output'
    out.mkdir(exist_ok=True)
    target = out / ('BrickLog-installable-debug.apk' if choice == '1' else 'BrickLog-unsigned-NOT-installable.apk')
    shutil.copy2(source, target)
    print(f'\nCreated: {target}')
    if choice == '1':
        print('Android automatically generated or reused a debug signing key. This APK is installable, but is not suitable for Play Store release.')
        print('It cannot update an app signed with a different key. Export and verify your backup before uninstalling.')
    else:
        print('This APK is UNSIGNED and cannot be installed on Android until signed.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError, RuntimeError, KeyboardInterrupt) as exc:
        print(f'Build stopped: {exc}', file=sys.stderr)
        sys.exit(1)
