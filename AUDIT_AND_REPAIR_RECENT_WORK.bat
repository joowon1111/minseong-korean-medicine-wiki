@echo off
chcp 65001 >nul
cd /d "%~dp0"
python AUDIT_AND_REPAIR_RECENT_WORK.py
pause
