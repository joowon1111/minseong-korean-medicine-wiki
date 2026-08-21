@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SEPARATE_FORMULA_ACUPOINT_ROLES.ps1"
