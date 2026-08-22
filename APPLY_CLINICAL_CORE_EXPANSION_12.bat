@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CLINICAL_CORE_EXPANSION_12.ps1"
pause
