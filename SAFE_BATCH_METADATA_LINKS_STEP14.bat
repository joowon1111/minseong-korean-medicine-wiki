@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SAFE_BATCH_METADATA_LINKS_STEP14.ps1"
