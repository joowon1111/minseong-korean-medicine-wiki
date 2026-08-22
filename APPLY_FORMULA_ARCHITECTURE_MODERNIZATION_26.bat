@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_FORMULA_ARCHITECTURE_MODERNIZATION_26.ps1"
pause
