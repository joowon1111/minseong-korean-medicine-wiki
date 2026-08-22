@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN_ACUPOINT_ATLAS_43_VALIDATION_FIXED.ps1"
pause
