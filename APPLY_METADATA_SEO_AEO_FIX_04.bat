@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_METADATA_SEO_AEO_FIX_04.ps1"
pause
