@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_CONDITION_NAV_10B_SAFE.py
pause
