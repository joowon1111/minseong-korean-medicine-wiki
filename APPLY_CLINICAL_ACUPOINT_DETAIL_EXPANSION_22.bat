@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CLINICAL_ACUPOINT_DETAIL_EXPANSION_22.ps1"
pause
