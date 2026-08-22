@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_ORPHAN_HUB_FIX_03_COMPLETE.ps1"
pause
