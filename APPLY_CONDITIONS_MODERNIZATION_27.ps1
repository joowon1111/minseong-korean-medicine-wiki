$ErrorActionPreference="Stop"
try{$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(!(Test-Path "docs\conditions")){throw "docs\conditions not found"}
$bk="_backup_conditions27_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
foreach($src in Get-ChildItem "_payload\docs\conditions" -File){$dest=Join-Path "docs\conditions" $src.Name;if(Test-Path $dest){Copy-Item $dest (Join-Path $bk $src.Name) -Force};Copy-Item $src.FullName $dest -Force}
New-Item -ItemType Directory -Force "_legacy_modernization"|Out-Null;Copy-Item "_payload\_legacy_modernization\LEGACY_MODERNIZATION_REPORT_27.md" "_legacy_modernization\LEGACY_MODERNIZATION_REPORT_27.md" -Force
Write-Host "CONDITIONS MODERNIZATION 27 COMPLETE" -ForegroundColor Green;Write-Host "8 condition pages rebuilt in place, not appended." -ForegroundColor Cyan;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"