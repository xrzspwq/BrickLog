@echo off
cd /d "%~dp0"
py -3 build-android.py
if errorlevel 1 echo Build failed. Read the message above.
pause
