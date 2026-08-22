@echo off
cd /d "%~dp0"
py -3 "%~dp0RUN_SECOND_QUALITY_AUDIT_30.py"
if errorlevel 1 python "%~dp0RUN_SECOND_QUALITY_AUDIT_30.py"
pause
