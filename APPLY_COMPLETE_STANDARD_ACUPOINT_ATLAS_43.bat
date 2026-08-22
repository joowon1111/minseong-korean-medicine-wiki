@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_COMPLETE_STANDARD_ACUPOINT_ATLAS_43.ps1"
pause
