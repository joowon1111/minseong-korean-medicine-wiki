@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_SUPPLEMENT_NATURAL_NAV_SAFE.py
pause
