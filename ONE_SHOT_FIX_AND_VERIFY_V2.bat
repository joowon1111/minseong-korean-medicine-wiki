@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==============================================
echo ONE-SHOT V2 실행 시작
echo ==============================================
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ONE_SHOT_FIX_AND_VERIFY_V2.ps1" > "%~dp0ONE_SHOT_RUN_LOG.txt" 2>&1
type "%~dp0ONE_SHOT_RUN_LOG.txt"
echo.
echo ==============================================
echo 실행 로그가 ONE_SHOT_RUN_LOG.txt 에 저장되었습니다.
echo 이 창은 자동으로 닫히지 않습니다.
echo ==============================================
pause
