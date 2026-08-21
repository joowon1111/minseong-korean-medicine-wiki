@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_COMBINATION_SEARCH_NAV_SAFE.py
pause
