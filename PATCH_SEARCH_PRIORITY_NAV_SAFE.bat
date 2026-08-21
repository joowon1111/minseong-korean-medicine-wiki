@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_SEARCH_PRIORITY_NAV_SAFE.py
pause
