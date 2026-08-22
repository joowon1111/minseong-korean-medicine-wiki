@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_STANDARD_ACUPOINT_ATLAS_NAV_44_YAML_FIX_V4.ps1"
pause
