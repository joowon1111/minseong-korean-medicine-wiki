@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo ONE-SHOT V3 START
echo ==============================================
echo.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0ONE_SHOT_FIX_AND_VERIFY_V3.ps1"
set "RC=%ERRORLEVEL%"
echo.
echo ==============================================
echo POWERSHELL EXIT CODE: %RC%
echo THIS WINDOW WILL STAY OPEN.
echo ==============================================
echo.
pause
endlocal
