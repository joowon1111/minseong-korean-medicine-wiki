@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_CONDITION_NAV_10E_SAFE.py
pause
