@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_MSK_NAV_10_SAFE.py
pause
