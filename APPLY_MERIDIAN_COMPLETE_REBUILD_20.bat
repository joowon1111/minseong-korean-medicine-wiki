@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_MERIDIAN_COMPLETE_REBUILD_20.ps1"
pause
