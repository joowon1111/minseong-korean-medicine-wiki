@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CLINICAL_REASONING_SAFETY_EVIDENCE_42.ps1"
pause
