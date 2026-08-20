@echo off
chcp 65001 >nul
cd /d "%~dp0"
python FIX_DEPLOY_STRICT.py
echo.
echo After this, commit and push the changed workflow file.
pause
