@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_SEARCH_HUB_NAV_SAFE.py
pause
