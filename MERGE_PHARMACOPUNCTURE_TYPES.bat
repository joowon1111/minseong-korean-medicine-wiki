@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_PHARMACOPUNCTURE_TYPES.py
pause
