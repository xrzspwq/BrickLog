@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv || goto fail
)
.venv\Scripts\python.exe -m pip install -r requirements.txt || goto fail
.venv\Scripts\python.exe main.py || goto fail
exit /b 0
:fail
echo BrickLog could not start. See the error above and README.md.
pause
exit /b 1
