@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_ACUPOINT_BRIDGE_NAV_SAFE.py
pause
