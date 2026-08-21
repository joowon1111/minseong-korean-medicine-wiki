@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_PEDIATRIC_PARENT_NAV_SAFE.py
pause
