@echo off
chcp 65001 >nul
cd /d "%~dp0"
python PATCH_HEAD_NECK_NEURO_NAV_SAFE.py
pause
