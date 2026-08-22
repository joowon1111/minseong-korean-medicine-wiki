@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_GOVERNANCE_DOCS_REFRESH_08.ps1"
pause
