@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_LEGACY_CORE_MODERNIZATION_24.ps1"
pause
