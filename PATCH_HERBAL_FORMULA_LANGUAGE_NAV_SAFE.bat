@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_HERBAL_FORMULA_LANGUAGE_NAV_SAFE.py
pause
