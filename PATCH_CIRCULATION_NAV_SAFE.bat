@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_CIRCULATION_NAV_SAFE.py
pause
