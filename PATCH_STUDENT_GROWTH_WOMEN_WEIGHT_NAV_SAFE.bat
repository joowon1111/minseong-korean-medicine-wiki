@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_STUDENT_GROWTH_WOMEN_WEIGHT_NAV_SAFE.py
pause
