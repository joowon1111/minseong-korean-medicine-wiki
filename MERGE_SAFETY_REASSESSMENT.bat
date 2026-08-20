@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_SAFETY_REASSESSMENT.py
pause
