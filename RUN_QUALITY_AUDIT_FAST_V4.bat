@echo off
title Minseong Wiki Quality Audit V4
cd /d "%~dp0"
echo.
echo ============================================
echo   Minseong Wiki Quality Audit FAST V4
echo ============================================
echo.
echo PowerShell audit starting...
echo Progress will be shown on this screen.
echo.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0RUN_QUALITY_AUDIT_FAST_V4.ps1"
echo.
echo Finished. Press any key to close.
pause >nul
