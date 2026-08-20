@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MERGE_FORMULA_HERB_LINKS.py
pause
