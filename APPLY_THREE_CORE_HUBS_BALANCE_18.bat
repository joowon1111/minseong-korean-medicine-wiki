@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_THREE_CORE_HUBS_BALANCE_18.ps1"
pause
