$ErrorActionPreference="Stop"
try{$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(!(Test-Path "docs\formula-architecture")){throw "docs\formula-architecture not found"}
$bk="_backup_formula_arch26_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
foreach($src in Get-ChildItem "_payload\docs\formula-architecture" -File){$dest=Join-Path "docs\formula-architecture" $src.Name;if(Test-Path $dest){Copy-Item $dest (Join-Path $bk $src.Name) -Force};Copy-Item $src.FullName $dest -Force}
Write-Host "FORMULA ARCHITECTURE MODERNIZATION 26 COMPLETE" -ForegroundColor Green
Write-Host "7 formula-family pages rebuilt in place, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"