@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_HERB_FORMULA_CATEGORY_MODERNIZATION_25.ps1"
pause
