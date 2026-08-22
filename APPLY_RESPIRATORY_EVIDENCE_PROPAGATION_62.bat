@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_RESPIRATORY_EVIDENCE_PROPAGATION_62.ps1"
pause
