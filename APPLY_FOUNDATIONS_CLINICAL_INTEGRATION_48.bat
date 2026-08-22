@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_FOUNDATIONS_CLINICAL_INTEGRATION_48.ps1"
pause
