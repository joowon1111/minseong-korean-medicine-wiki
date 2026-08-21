@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_ELDERLY_RECOVERY_NAV_SAFE.py
pause
