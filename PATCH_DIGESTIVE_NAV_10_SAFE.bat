@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_DIGESTIVE_NAV_10_SAFE.py
pause
