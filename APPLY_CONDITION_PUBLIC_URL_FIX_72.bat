@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CONDITION_PUBLIC_URL_FIX_72.ps1"
pause
