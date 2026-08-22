$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_thin05_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
$rows=Import-Csv "thin05_manifest.tsv" -Delimiter "`t";$changed=0
foreach($row in $rows){
 $p=Join-Path "docs" ($row.path.Replace("/","\"))
 if(-not(Test-Path $p)){continue}
 $t=Get-Content $p -Raw -Encoding UTF8
 if($t.Contains("<!-- QUALITY_DEPTH_05_START -->")){continue}
 $dest=Join-Path $bk ($row.path.Replace("/","\"))
 $dd=Split-Path $dest -Parent;if(-not(Test-Path $dd)){New-Item -ItemType Directory -Force $dd|Out-Null}
 Copy-Item $p $dest -Force
 $block=Get-Content (Join-Path "_thin05_payload" $row.blockfile) -Raw -Encoding UTF8
 Set-Content $p ($t.TrimEnd()+"`r`n`r`n"+$block+"`r`n") -Encoding UTF8
 $changed++
}
Write-Host ("THIN CONTENT EVIDENCE UPGRADE 05 COMPLETE: "+$changed+" pages") -ForegroundColor Green
Write-Host "Only genuinely sparse priority conditions/formulas/herbs were enriched." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
