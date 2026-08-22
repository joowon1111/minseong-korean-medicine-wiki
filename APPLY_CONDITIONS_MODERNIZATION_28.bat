@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CONDITIONS_MODERNIZATION_28.ps1"
pause
