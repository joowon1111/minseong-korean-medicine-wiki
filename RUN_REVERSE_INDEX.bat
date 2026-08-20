@echo off
chcp 65001 >nul
cd /d "%~dp0"
python BUILD_HERB_REVERSE_INDEX.py
if errorlevel 1 (
 echo.
 echo 오류가 발생했습니다. Commit하지 말고 화면을 보여주세요.
 pause
 exit /b 1
)
echo.
echo 완료되었습니다.
echo Commit: Build reverse herb to Sasang formula knowledge graph
pause
