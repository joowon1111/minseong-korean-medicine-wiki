@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_HERBAL_FORMULA_CLINICAL_MODERNIZATION_50.ps1"
pause
