@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CONCEPTS_DIAGNOSTICS_MODERNIZATION_36.ps1"
pause
