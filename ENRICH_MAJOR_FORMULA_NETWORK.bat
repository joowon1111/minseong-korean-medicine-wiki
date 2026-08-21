@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ENRICH_MAJOR_FORMULA_NETWORK.ps1"
