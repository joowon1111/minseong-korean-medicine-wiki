$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs\herbal-formula-clinical")){throw "docs\herbal-formula-clinical not found"}
$bk="_backup_herbal_formula_clinical50_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
$n=0
foreach($s in Get-ChildItem "_payload\docs\herbal-formula-clinical" -File){
 $d=Join-Path "docs\herbal-formula-clinical" $s.Name
 if(Test-Path $d){Copy-Item $d (Join-Path $bk $s.Name) -Force}
 Copy-Item $s.FullName $d -Force;$n++
}
Write-Host "HERBAL FORMULA CLINICAL MODERNIZATION 50 COMPLETE" -ForegroundColor Green
Write-Host ("Updated pages: "+$n) -ForegroundColor Cyan
Write-Host "Symptoms, patterns, herbs, formula architecture, and evidence are now clinically connected." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"