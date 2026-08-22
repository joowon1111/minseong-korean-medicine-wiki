@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_DUPLICATE_LAYER_CONSOLIDATION_37.ps1"
pause
