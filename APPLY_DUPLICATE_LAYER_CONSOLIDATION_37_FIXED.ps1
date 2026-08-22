$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
$Status=Join-Path $R "APPLY_37_STATUS.txt"
try{
  "STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Set-Content $Status -Encoding UTF8
  if(!(Test-Path "docs")){throw "docs not found. Extract this ZIP into the repository root beside docs and mkdocs.yml."}

  $bk="_backup_duplicate_consolidation37_"+(Get-Date -Format "yyyyMMdd-HHmmss")
  New-Item -ItemType Directory -Force $bk|Out-Null

  foreach($s in Get-ChildItem "_payload\docs" -Recurse -File){
    $rel=$s.FullName.Substring((Resolve-Path "_payload\docs").Path.Length+1)
    $d=Join-Path "docs" $rel
    $dir=Split-Path $d -Parent
    if(!(Test-Path $dir)){New-Item -ItemType Directory -Force $dir|Out-Null}
    if(Test-Path $d){
      Copy-Item $d (Join-Path $bk ($rel.Replace("\","_"))) -Force
    }
    Copy-Item $s.FullName $d -Force
  }

  @(
    "COMPLETE"
    "Applied: duplicate legacy URL consolidation"
    "Backup: $bk"
    "Audit script remains in repository root: RUN_DUPLICATE_AWARE_AUDIT_37.py"
  ) | Set-Content $Status -Encoding UTF8

  Write-Host "DUPLICATE LAYER CONSOLIDATION 37 FIXED COMPLETE" -ForegroundColor Green
  Write-Host "Legacy duplicate URLs now point to canonical detailed pages." -ForegroundColor Cyan
  Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
  Write-Host "Next: Commit / Push. After green deployment, optionally run RUN_DUPLICATE_AWARE_AUDIT_37_FIXED.bat." -ForegroundColor Cyan
}catch{
  @(
    "FAILED"
    $_.Exception.Message
    ($_ | Out-String)
  ) | Set-Content $Status -Encoding UTF8
  Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
  Write-Host "See APPLY_37_STATUS.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"
