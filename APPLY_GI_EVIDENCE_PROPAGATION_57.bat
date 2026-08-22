@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_GI_EVIDENCE_PROPAGATION_57.ps1"
pause
