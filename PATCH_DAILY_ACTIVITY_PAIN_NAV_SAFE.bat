@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_DAILY_ACTIVITY_PAIN_NAV_SAFE.py
pause
