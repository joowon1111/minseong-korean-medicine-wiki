@echo off
chcp 65001 >nul
cd /d "%~dp0"
python FINALIZE_SEARCH_KEYWORDS.py
pause
