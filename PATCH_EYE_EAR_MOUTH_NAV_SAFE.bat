@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_EYE_EAR_MOUTH_NAV_SAFE.py
pause
