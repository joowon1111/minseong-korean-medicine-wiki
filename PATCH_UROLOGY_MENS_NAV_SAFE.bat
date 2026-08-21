@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_UROLOGY_MENS_NAV_SAFE.py
pause
