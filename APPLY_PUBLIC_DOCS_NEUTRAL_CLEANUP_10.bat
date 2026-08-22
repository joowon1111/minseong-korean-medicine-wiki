@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_PUBLIC_DOCS_NEUTRAL_CLEANUP_10.ps1"
pause
