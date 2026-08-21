@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_SASANG_PATIENT_NAV_SAFE.py
pause
