@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN_DUPLICATE_AWARE_AUDIT_37_FIXED.ps1"
pause
