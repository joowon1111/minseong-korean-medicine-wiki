$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\acupoint-network\by-condition.md")){throw "docs\acupoint-network\by-condition.md not found"}
$bk="_backup_meridian_symptom23_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
Copy-Item "docs\acupoint-network\by-condition.md" (Join-Path $bk "by-condition.md") -Force
Copy-Item "_payload\by-condition.md" "docs\acupoint-network\by-condition.md" -Force
Write-Host "MERIDIAN SYMPTOM MAP REBUILD 23 COMPLETE" -ForegroundColor Green
Write-Host "Existing symptom map was replaced and integrated, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
