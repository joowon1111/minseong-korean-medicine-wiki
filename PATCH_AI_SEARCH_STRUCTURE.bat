@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_AI_SEARCH_STRUCTURE.py
pause
