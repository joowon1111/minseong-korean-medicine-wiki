@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_EXTRAORDINARY_VESSELS_MODERNIZATION_32.ps1"
pause
