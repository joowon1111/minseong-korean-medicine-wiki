$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\meridian-network\index.md")){throw "20단계 경락 허브가 없습니다."}
if(!(Test-Path "docs\acupoint-network\index.md")){throw "20단계 경혈 허브가 없습니다."}
$bk="_backup_special_points21_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
Copy-Item "docs\meridian-network\index.md" (Join-Path $bk "meridian-index.md") -Force
Copy-Item "docs\acupoint-network\index.md" (Join-Path $bk "acupoint-index.md") -Force
if(Test-Path "docs\meridian-network\special-points"){Copy-Item "docs\meridian-network\special-points" (Join-Path $bk "special-points") -Recurse -Force}

New-Item -ItemType Directory -Force "docs\meridian-network\special-points"|Out-Null
Copy-Item "_payload\meridian-network\special-points\*" "docs\meridian-network\special-points\" -Force
Copy-Item "_payload\meridian-network\index.md" "docs\meridian-network\index.md" -Force
Copy-Item "_payload\acupoint-network\index.md" "docs\acupoint-network\index.md" -Force

Write-Host "SPECIAL POINT SYSTEM COMPLETE 21 COMPLETE" -ForegroundColor Green
Write-Host "Specific-point system was integrated into existing meridian/acupoint hubs, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
