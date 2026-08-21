@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_HEALTH_CHECKUP_NAV_SAFE.py
pause
