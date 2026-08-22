$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs")){throw "docs not found"}
$bk="_backup_foundations48_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
$count=0
foreach($s in Get-ChildItem "_payload\docs" -Recurse -File){
 $rel=$s.FullName.Substring((Resolve-Path "_payload\docs").Path.Length+1);$d=Join-Path "docs" $rel;$dir=Split-Path $d -Parent
 if(!(Test-Path $dir)){New-Item -ItemType Directory -Force $dir|Out-Null}
 if(Test-Path $d){Copy-Item $d (Join-Path $bk ($rel.Replace("\","_"))) -Force}
 Copy-Item $s.FullName $d -Force;$count++
}
Write-Host "FOUNDATIONS CLINICAL INTEGRATION 48 COMPLETE" -ForegroundColor Green
Write-Host ("Updated pages: "+$count) -ForegroundColor Cyan
Write-Host "Foundational theory now connects directly to pattern differentiation and treatment." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"