@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_ACU_SAFETY_MODALITIES.py
pause
