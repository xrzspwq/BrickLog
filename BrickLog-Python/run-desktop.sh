#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  if [ "$(uname -s)" = Linux ] && [ -x /usr/bin/python3 ]; then /usr/bin/python3 -m venv --system-site-packages .venv
  else python3 -m venv --system-site-packages .venv; fi
fi
.venv/bin/python -m pip install -r requirements.txt
exec .venv/bin/python main.py
