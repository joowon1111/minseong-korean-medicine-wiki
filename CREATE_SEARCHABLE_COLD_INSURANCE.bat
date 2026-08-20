@echo off
chcp 65001 >nul
cd /d "%~dp0"
python CREATE_SEARCHABLE_COLD_INSURANCE.py
pause
