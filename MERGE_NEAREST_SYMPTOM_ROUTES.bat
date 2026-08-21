@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_NEAREST_SYMPTOM_ROUTES.py
pause
