@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_THIN_CONTENT_EVIDENCE_UPGRADE_05.ps1"
pause
