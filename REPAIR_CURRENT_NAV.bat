@echo off
chcp 65001 >nul
cd /d "%~dp0"
python REPAIR_CURRENT_NAV.py
if errorlevel 1 (
 echo.
 echo 오류가 발생했습니다. Commit하지 말고 화면을 보여주세요.
 pause
 exit /b 1
)
echo.
echo 완료. GitHub Desktop에서 mkdocs.yml 변경을 Commit/Push 하세요.
pause
