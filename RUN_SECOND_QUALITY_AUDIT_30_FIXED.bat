@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN_SECOND_QUALITY_AUDIT_30_FIXED.ps1"
pause
