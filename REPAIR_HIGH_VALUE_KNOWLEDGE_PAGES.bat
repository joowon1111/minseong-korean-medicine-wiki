@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0REPAIR_HIGH_VALUE_KNOWLEDGE_PAGES.ps1"
