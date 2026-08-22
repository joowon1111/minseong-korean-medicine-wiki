@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_SPECIAL_POINT_SYSTEM_COMPLETE_21.ps1"
pause
