@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ENRICH_CORE_HUB_CONTENT_METADATA.ps1"
