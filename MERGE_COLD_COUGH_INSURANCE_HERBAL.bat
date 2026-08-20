@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_COLD_COUGH_INSURANCE_HERBAL.py
pause
