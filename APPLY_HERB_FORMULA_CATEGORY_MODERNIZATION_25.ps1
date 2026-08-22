$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\herbs\categories")){throw "docs\herbs\categories not found"}
if(!(Test-Path "docs\formulas\categories")){throw "docs\formulas\categories not found"}
$bk="_backup_category_modernization25_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null

foreach($src in Get-ChildItem "_payload\docs\herbs\categories" -File){
 $dest=Join-Path "docs\herbs\categories" $src.Name
 if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ("herbs_"+$src.Name)) -Force}
 Copy-Item $src.FullName $dest -Force
}
foreach($src in Get-ChildItem "_payload\docs\formulas\categories" -File){
 $dest=Join-Path "docs\formulas\categories" $src.Name
 if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ("formulas_"+$src.Name)) -Force}
 Copy-Item $src.FullName $dest -Force
}
New-Item -ItemType Directory -Force "_legacy_modernization"|Out-Null
Copy-Item "_payload\_legacy_modernization\LEGACY_MODERNIZATION_REPORT_25.md" "_legacy_modernization\LEGACY_MODERNIZATION_REPORT_25.md" -Force

Write-Host "HERB FORMULA CATEGORY MODERNIZATION 25 COMPLETE" -ForegroundColor Green
Write-Host "14 legacy category pages were rebuilt in place, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
