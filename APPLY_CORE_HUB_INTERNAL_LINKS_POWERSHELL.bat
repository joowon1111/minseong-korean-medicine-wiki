@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0APPLY_CORE_HUB_INTERNAL_LINKS_POWERSHELL.ps1"
