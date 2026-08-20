@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_HERBAL_INTO_SYMPTOMS.py
pause
