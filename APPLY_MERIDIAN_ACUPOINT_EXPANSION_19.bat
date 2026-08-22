@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_MERIDIAN_ACUPOINT_EXPANSION_19.ps1"
pause
