$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\acupuncture\points")){throw "docs\acupuncture\points not found"}
$bk="_backup_core_acupoints33_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
foreach($src in Get-ChildItem "_payload\docs\acupuncture\points" -File){
 $dest=Join-Path "docs\acupuncture\points" $src.Name
 if(Test-Path $dest){Copy-Item $dest (Join-Path $bk $src.Name) -Force}
 Copy-Item $src.FullName $dest -Force
}
Write-Host "CORE ACUPOINT MODERNIZATION 33 COMPLETE" -ForegroundColor Green
Write-Host "12 high-priority acupoint pages rebuilt in place, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
