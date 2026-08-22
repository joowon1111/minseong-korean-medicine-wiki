@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN_FULL_QUALITY_AUDIT_V3.ps1"
pause
