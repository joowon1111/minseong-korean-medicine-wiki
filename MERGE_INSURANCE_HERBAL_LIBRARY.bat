@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_INSURANCE_HERBAL_LIBRARY.py
pause
