@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_PATTERN_DIFFERENTIAL_EXPANSION_16.ps1"
pause
