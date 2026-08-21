@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_COMBINED_SYMPTOM_SEARCH.py
pause
