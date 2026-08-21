@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_MUSCLE_STIFFNESS_NAV_SAFE.py
pause
