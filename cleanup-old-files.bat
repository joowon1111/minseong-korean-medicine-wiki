@echo off
echo Removing stale duplicate files from earlier wiki structure...
for %%F in (
"docs\basic\index.md"
"docs\basic\blood-deficiency.md"
"docs\basic\blood-stasis.md"
"docs\basic\phlegm-fluid.md"
"docs\basic\qi-deficiency.md"
"docs\classics\guizhi-indication.md"
"docs\classics\mahuang-indication.md"
"docs\classics\taiyang-definition.md"
"docs\classics\xiaochaihu-indication.md"
"docs\diseases\index.md"
"docs\diseases\chronic-fatigue.md"
"docs\diseases\dyspepsia.md"
"docs\diseases\insomnia.md"
"docs\diseases\low-back-pain.md"
) do (
  if exist %%F del %%F
)
if exist "docs\basic" rmdir "docs\basic" 2>nul
if exist "docs\diseases" rmdir "docs\diseases" 2>nul
echo Cleanup complete.
pause
