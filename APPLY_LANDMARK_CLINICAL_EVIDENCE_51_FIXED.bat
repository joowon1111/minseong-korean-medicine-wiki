@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_LANDMARK_CLINICAL_EVIDENCE_51_FIXED.ps1"
pause
