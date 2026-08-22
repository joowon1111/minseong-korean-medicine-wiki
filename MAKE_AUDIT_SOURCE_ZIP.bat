@echo off
title Minseong Wiki Audit Source Collector
cd /d "%~dp0"
echo Starting...
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0MAKE_AUDIT_SOURCE_ZIP.ps1"
pause
