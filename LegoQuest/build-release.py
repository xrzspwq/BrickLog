#!/usr/bin/env python3
"""Interactively sign a release APK without writing passwords to the project."""
from getpass import getpass
from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DEFAULT = Path.home() / '.bricklog' / 'bricklog-release.p12'


def run(command, **kwargs):
    subprocess.run(command, cwd=ROOT, check=True, **kwargs)


def main():
    print('BrickLog signed Android release')
    print('Requirements: JDK 17 or 21, Android SDK 35, internet on the first build.')
    print('Keep your release keystore and password safe: the same key is needed for future updates.')
    name = input(f'Keystore path [{DEFAULT}]: ').strip() or str(DEFAULT)
    path = Path(name).expanduser().resolve()
    if ROOT in path.parents:
        raise ValueError('Keep the keystore outside the project folder so it is not accidentally shared.')
    alias = input('Key alias [bricklog]: ').strip() or 'bricklog'
    store_password = getpass('Keystore password: ')
    if len(store_password) < 6:
        raise ValueError('The keystore password must be at least 6 characters.')
    env = os.environ.copy()
    env.update(BRICKLOG_KEYSTORE=str(path), BRICKLOG_STORE_PASSWORD=store_password,
               BRICKLOG_KEY_ALIAS=alias, BRICKLOG_KEY_PASSWORD=store_password)
    if not path.exists():
        print(f'No keystore exists at {path}.')
        if input('Create a new personal signing key there? [y/N] ').strip().lower() != 'y':
            raise ValueError('Cancelled; no key was created.')
        if getpass('Confirm keystore password: ') != store_password:
            raise ValueError('Passwords do not match.')
        keytool = Path(os.environ['JAVA_HOME']) / 'bin' / ('keytool.exe' if os.name == 'nt' else 'keytool') if os.environ.get('JAVA_HOME') else 'keytool'
        path.parent.mkdir(parents=True, exist_ok=True)
        run([str(keytool), '-genkeypair', '-noprompt', '-keystore', str(path), '-storetype', 'PKCS12',
             '-storepass:env', 'BRICKLOG_STORE_PASSWORD', '-keypass:env', 'BRICKLOG_KEY_PASSWORD',
             '-alias', alias, '-keyalg', 'RSA', '-keysize', '3072', '-validity', '10000',
             '-dname', 'CN=BrickLog Owner, OU=Personal, O=Personal, C=US'], env=env)
        print('Created the keystore. Back it up privately, along with its password.')
    else:
        print('Using existing keystore. This script assumes the key password equals the keystore password.')
    wrapper = ROOT / ('gradlew.bat' if os.name == 'nt' else 'gradlew')
    cmd = ['cmd', '/d', '/c', str(wrapper), '--no-daemon', 'assembleRelease'] if os.name == 'nt' else [str(wrapper), '--no-daemon', 'assembleRelease']
    run(cmd, env=env)
    apk = ROOT / 'app' / 'build' / 'outputs' / 'apk' / 'release' / 'app-release.apk'
    if not apk.exists():
        raise RuntimeError('Release APK was not produced. Check the build output.')
    output = ROOT / 'release-output'
    output.mkdir(exist_ok=True)
    target = output / 'BrickLog-release.apk'
    shutil.copy2(apk, target)
    print(f'\nSigned APK: {target}\nBack up the keystore and password separately. Do not share the keystore.')
    print('An installed app signed by a different key cannot be updated by this APK. Export a JSON backup first.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError, RuntimeError, KeyboardInterrupt) as exc:
        print(f'Build stopped: {exc}', file=sys.stderr)
        sys.exit(1)
