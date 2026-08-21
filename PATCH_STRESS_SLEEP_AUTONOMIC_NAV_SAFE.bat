@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_STRESS_SLEEP_AUTONOMIC_NAV_SAFE.py
pause
