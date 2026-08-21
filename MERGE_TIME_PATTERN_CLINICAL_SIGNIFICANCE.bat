@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_TIME_PATTERN_CLINICAL_SIGNIFICANCE.py
pause
