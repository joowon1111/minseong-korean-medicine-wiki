@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_PATIENT_FRIENDLY_DIFFERENTIALS.py
pause
