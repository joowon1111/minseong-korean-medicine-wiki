@echo off
cd /d "%~dp0"
py -3 "%~dp0RUN_DUPLICATE_AWARE_AUDIT_37.py"
if errorlevel 1 python "%~dp0RUN_DUPLICATE_AWARE_AUDIT_37.py"
pause
