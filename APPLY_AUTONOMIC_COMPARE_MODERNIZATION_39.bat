@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_AUTONOMIC_COMPARE_MODERNIZATION_39.ps1"
pause
