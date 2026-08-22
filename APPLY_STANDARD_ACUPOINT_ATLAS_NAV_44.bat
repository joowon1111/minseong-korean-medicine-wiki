@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_STANDARD_ACUPOINT_ATLAS_NAV_44.ps1"
pause
