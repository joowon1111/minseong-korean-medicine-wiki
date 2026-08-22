$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\formula-architecture")){throw "docs\formula-architecture not found"}
$bk="_backup_formula_architecture47_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
$count=0
foreach($s in Get-ChildItem "_payload\docs\formula-architecture" -File){
 $d=Join-Path "docs\formula-architecture" $s.Name
 if(Test-Path $d){Copy-Item $d (Join-Path $bk $s.Name) -Force}
 Copy-Item $s.FullName $d -Force
 $count++
}
Write-Host "FORMULA ARCHITECTURE MODERNIZATION 47 COMPLETE" -ForegroundColor Green
Write-Host ("Updated pages: "+$count) -ForegroundColor Cyan
Write-Host "Core formula families rebuilt as differential clinical structures." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"