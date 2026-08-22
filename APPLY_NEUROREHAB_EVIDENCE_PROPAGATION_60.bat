@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_NEUROREHAB_EVIDENCE_PROPAGATION_60.ps1"
pause
