@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_LINKFIX_SPECIALPOINT_MODERNIZATION_31.ps1"
pause
