@echo off
chcp 65001 >nul
cd /d "%~dp0"
python APPLY_BALANCED_SUPPLEMENT_PAGES.py
pause
