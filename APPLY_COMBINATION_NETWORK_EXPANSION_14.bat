@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_COMBINATION_NETWORK_EXPANSION_14.ps1"
pause
