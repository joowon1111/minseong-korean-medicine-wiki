@echo off
chcp 65001 >nul
cd /d "%~dp0"
python APPLY_SEARCH_PRIORITY_METADATA.py
pause
