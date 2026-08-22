@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0APPLY_STANDARD_ACUPOINT_ATLAS_NAV_44_YAML_FIX.py"
) else (
  python "%~dp0APPLY_STANDARD_ACUPOINT_ATLAS_NAV_44_YAML_FIX.py"
)
if errorlevel 1 (
  echo.
  echo FIX FAILED. See APPLY_44_YAML_FIX_STATUS.txt
  pause
  exit /b 1
)
echo.
echo Running local MkDocs build check...
python -m mkdocs build
if errorlevel 1 (
  echo.
  echo YAML fix applied, but local MkDocs build still failed.
  echo Please send the visible error before committing.
  pause
  exit /b 1
)
echo.
echo STANDARD ACUPOINT ATLAS NAV 44 BUILD CHECK COMPLETE
pause
