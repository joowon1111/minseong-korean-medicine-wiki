$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\acupoint-network\index.md")){throw "acupoint-network index not found"}
if(!(Test-Path "docs\meridian-network\special-points\index.md")){throw "21단계 특정혈 지식망이 없습니다."}
$bk="_backup_acupoint_detail22_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
Copy-Item "docs\acupoint-network\index.md" (Join-Path $bk "acupoint-index.md") -Force

New-Item -ItemType Directory -Force "docs\acupuncture\points"|Out-Null
foreach($x in Get-ChildItem "_payload\acupuncture\points" -File){
 $dest=Join-Path "docs\acupuncture\points" $x.Name
 if(Test-Path $dest){Copy-Item $dest (Join-Path $bk $x.Name) -Force}
 Copy-Item $x.FullName $dest -Force
}
Copy-Item "_payload\acupoint-network\index.md" "docs\acupoint-network\index.md" -Force

Write-Host "CLINICAL ACUPOINT DETAIL EXPANSION 22 COMPLETE" -ForegroundColor Green
Write-Host "32 detailed point pages integrated into the existing acupoint hub." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
