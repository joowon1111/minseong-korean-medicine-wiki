@echo off
chcp 65001 >nul
cd /d "%~dp0"
python REGISTER_GENERAL_FORMULARY.py
if errorlevel 1 (
 echo 오류가 발생했습니다. Commit하지 말고 화면을 보여주세요.
 pause
 exit /b 1
)
echo.
echo 일반 방제 NAV 등록 완료
pause
