@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_MERIDIAN_SYMPTOM_MAP_REBUILD_23.ps1"
pause
