@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_PUBLIC_GOVERNANCE_CLEANUP_09.ps1"
pause
