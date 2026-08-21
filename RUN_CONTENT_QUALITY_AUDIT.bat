@echo off
chcp 65001 >nul
cd /d "%~dp0"
python RUN_CONTENT_QUALITY_AUDIT.py
pause
