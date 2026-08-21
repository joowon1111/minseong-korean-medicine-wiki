@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_TONIC_INTENT_NAV_SAFE.py
pause
