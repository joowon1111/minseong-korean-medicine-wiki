@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_WOMENS_LIFECYCLE_NAV_SAFE.py
pause
