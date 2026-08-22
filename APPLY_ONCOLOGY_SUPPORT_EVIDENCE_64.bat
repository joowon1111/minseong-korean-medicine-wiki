@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_ONCOLOGY_SUPPORT_EVIDENCE_64.ps1"
pause
