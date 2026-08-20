@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_MORE_FORMULAS_INTO_CONDITIONS.py
pause
