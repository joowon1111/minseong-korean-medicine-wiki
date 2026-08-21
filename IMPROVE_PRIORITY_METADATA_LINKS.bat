@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0IMPROVE_PRIORITY_METADATA_LINKS.ps1"
