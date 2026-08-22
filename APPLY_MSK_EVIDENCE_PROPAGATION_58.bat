@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_MSK_EVIDENCE_PROPAGATION_58.ps1"
pause
