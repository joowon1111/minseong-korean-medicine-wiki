@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_FAQ_LINKS.py
pause
