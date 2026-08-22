@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CORE_ACUPOINT_MODERNIZATION_33.ps1"
pause
