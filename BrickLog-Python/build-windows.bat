@echo off
setlocal
cd /d "%~dp0"
if not exist ..\LegoQuest\app\src\main\assets\index.html goto missingassets
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv || goto fail
)
.venv\Scripts\python.exe -m pip install -r requirements-build.txt || goto fail
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm bricklog.spec || goto fail
if not exist release-output mkdir release-output
powershell -NoProfile -Command "Compress-Archive -Path 'dist\BrickLog' -DestinationPath 'release-output\BrickLog-Windows.zip' -Force" || goto fail
echo.
echo Created release-output\BrickLog-Windows.zip. Extract it and run BrickLog\BrickLog.exe.
echo Keep the entire folder together. Requires Microsoft Edge WebView2 Runtime.
pause
exit /b 0
:missingassets
echo Missing shared assets. Keep LegoQuest next to BrickLog-Python.
:fail
echo Build failed. See the error above and README.md.
pause
exit /b 1
