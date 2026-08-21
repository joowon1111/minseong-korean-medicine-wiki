@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_ACUPUNCTURE_QUESTION_NAV_SAFE.py
pause
