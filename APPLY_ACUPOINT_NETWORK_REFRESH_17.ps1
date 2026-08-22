$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs\acupoint-network.md")){throw "docs\acupoint-network.md not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_acupoint_network17_"+$stamp
New-Item -ItemType Directory -Force $bk|Out-Null
Copy-Item "docs\acupoint-network.md" (Join-Path $bk "acupoint-network.md") -Force
Copy-Item "_payload\acupoint-network.md" "docs\acupoint-network.md" -Force
Write-Host "ACUPOINT NETWORK REFRESH 17 COMPLETE" -ForegroundColor Green
Write-Host "Expanded representative points, symptom pathways, combinations, patterns, formula links and evidence navigation." -ForegroundColor Green
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{
Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
