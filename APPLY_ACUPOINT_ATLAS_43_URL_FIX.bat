@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_ACUPOINT_ATLAS_43_URL_FIX.ps1"
pause
