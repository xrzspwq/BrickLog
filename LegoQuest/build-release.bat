@echo off
cd /d "%~dp0"
py -3 build-release.py
if errorlevel 1 echo Release build failed. Read the message above.
pause
