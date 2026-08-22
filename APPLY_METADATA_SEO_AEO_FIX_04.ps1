$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_metadata_04_"+$stamp
New-Item -ItemType Directory -Force $bk|Out-Null
$rows=Import-Csv "metadata_patch.tsv" -Delimiter "`t"
$changed=0
foreach($row in $rows){
 $p=Join-Path "docs" ($row.path.Replace("/","\"))
 if(-not(Test-Path $p)){continue}
 $t=Get-Content $p -Raw -Encoding UTF8
 # Safety: only touch documents still lacking YAML front matter.
 if($t.StartsWith("---")){continue}
 $rel=$row.path.Replace("/","\")
 $dest=Join-Path $bk $rel
 $dd=Split-Path $dest -Parent
 if(-not(Test-Path $dd)){New-Item -ItemType Directory -Force $dd|Out-Null}
 Copy-Item $p $dest -Force
 $tagLines=($row.tags -split ",")|ForEach-Object{"  - "+$_}
 $fm="---`r`ntitle: `"$($row.title.Replace('"',''))`"`r`ndescription: `"$($row.description.Replace('"',''))`"`r`ntags:`r`n"+($tagLines -join "`r`n")+"`r`n---`r`n`r`n"
 Set-Content $p ($fm+$t) -Encoding UTF8
 $changed++
}
Write-Host ("METADATA SEO/AEO FIX 04 COMPLETE: "+$changed+" documents") -ForegroundColor Green
Write-Host "Only priority conditions/formulas/herbs pages without front matter were changed." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
