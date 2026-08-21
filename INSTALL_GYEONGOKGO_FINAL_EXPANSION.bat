@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL_GYEONGOKGO_FINAL_EXPANSION.ps1"
pause
