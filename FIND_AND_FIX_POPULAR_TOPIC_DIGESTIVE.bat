@echo off
chcp 65001 >nul
cd /d "%~dp0"
python FIND_AND_FIX_POPULAR_TOPIC_DIGESTIVE.py
pause
