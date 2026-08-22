$ErrorActionPreference="Stop"
try{$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_public_cleanup09_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
$map=@{"seo-aeo-standard.md"="docs\seo-aeo-standard.md";"metadata-audit-guide.md"="docs\metadata-audit-guide.md";"site-structure.md"="docs\ai\site-structure.md"}
foreach($k in $map.Keys){$d=$map[$k];if(Test-Path $d){Copy-Item $d (Join-Path $bk ($d.Replace("\","_"))) -Force};Copy-Item (Join-Path "_public_docs_payload" $k) $d -Force}
Write-Host "PUBLIC GOVERNANCE CLEANUP 09 COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"