@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_PATTERN_SYNDROME_NETWORK_EXPANSION_15.ps1"
pause
