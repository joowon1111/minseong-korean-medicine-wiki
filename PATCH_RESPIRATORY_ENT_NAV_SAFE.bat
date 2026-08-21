@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_RESPIRATORY_ENT_NAV_SAFE.py
pause
