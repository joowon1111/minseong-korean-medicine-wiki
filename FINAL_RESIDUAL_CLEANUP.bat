@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo FINAL RESIDUAL CLEANUP START
echo ==============================================
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0FINAL_RESIDUAL_CLEANUP.ps1"
set "RC=%ERRORLEVEL%"
echo.
echo POWERSHELL EXIT CODE: %RC%
echo THIS WINDOW WILL STAY OPEN.
pause
endlocal
