@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_HOME_POPULAR_TOPIC_DIGESTIVE.py
pause
