@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_ACUPOINT_NETWORK_REFRESH_17.ps1"
pause
