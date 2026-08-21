@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_SKIN_ALLERGY_NAV_SAFE.py
pause
