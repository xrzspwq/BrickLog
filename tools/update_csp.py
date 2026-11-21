#!/usr/bin/env python3
"""Update the CSP script hashes after intentional edits to the shared UI."""
import base64
import hashlib
from pathlib import Path
import re

p = Path(__file__).resolve().parent.parent / 'LegoQuest/app/src/main/assets/index.html'
s = p.read_text(encoding='utf-8')
scripts = re.findall(r'<script>(.*?)</script>', s, re.S)
if len(scripts) != 2:
    raise SystemExit('Expected exactly two inline scripts; inspect the policy manually.')
hashes = ' '.join("'sha256-" + base64.b64encode(hashlib.sha256(script.encode('utf-8')).digest()).decode('ascii') + "'" for script in scripts)
s, n = re.subn(r"script-src [^;]+;", "script-src 'unsafe-eval' " + hashes + ';', s, count=1)
if n != 1:
    raise SystemExit('Could not find the CSP script-src directive.')
p.write_text(s, encoding='utf-8')
print('Updated the CSP script hashes.')
