$ErrorActionPreference="Stop"
try{$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(!(Test-Path "docs\meridian-network\index.md")){throw "docs\meridian-network\index.md not found"};if(!(Test-Path "docs\acupoint-network\index.md")){throw "docs\acupoint-network\index.md not found"}
$bk="_backup_meridian_complete20_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
Copy-Item "docs\meridian-network" (Join-Path $bk "meridian-network") -Recurse -Force;Copy-Item "docs\acupoint-network" (Join-Path $bk "acupoint-network") -Recurse -Force
Copy-Item "_payload\meridian-network\*" "docs\meridian-network\" -Force;Copy-Item "_payload\acupoint-network\index.md" "docs\acupoint-network\index.md" -Force
Write-Host "MERIDIAN COMPLETE REBUILD 20 COMPLETE" -ForegroundColor Green;Write-Host "Existing hubs were integrated/replaced, not appended." -ForegroundColor Cyan;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"