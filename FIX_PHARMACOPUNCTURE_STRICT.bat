@echo off
chcp 65001 >nul
cd /d "%~dp0"
python FIX_PHARMACOPUNCTURE_STRICT.py
echo.
echo Now run: mkdocs build --strict
pause
