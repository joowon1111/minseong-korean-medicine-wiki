$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs\answer-guides")){throw "docs\answer-guides not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_cannibal06_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
$rows=Import-Csv "cannibal_manifest.tsv" -Delimiter "`t";$changed=0
foreach($row in $rows){
 $p=Join-Path "docs" ($row.path.Replace("/","\"))
 if(-not(Test-Path $p)){continue}
 $t=Get-Content $p -Raw -Encoding UTF8
 $block=Get-Content (Join-Path "_cannibal_payload" $row.blockfile) -Raw -Encoding UTF8
 $s="<!-- SEARCH_INTENT_DIFFERENTIATION_06_START -->";$e="<!-- SEARCH_INTENT_DIFFERENTIATION_06_END -->"
 $dest=Join-Path $bk ($row.path.Replace("/","\"));$dd=Split-Path $dest -Parent
 if(-not(Test-Path $dd)){New-Item -ItemType Directory -Force $dd|Out-Null};Copy-Item $p $dest -Force
 if($t.Contains($s)){
  $pat=[regex]::Escape($s)+".*?"+[regex]::Escape($e)
  $t=[regex]::Replace($t,$pat,$block,[Text.RegularExpressions.RegexOptions]::Singleline)
 }else{$t=$t.TrimEnd()+"`r`n`r`n"+$block+"`r`n"}
 Set-Content $p $t -Encoding UTF8;$changed++
}
Write-Host ("CANNIBALIZATION FIX 06 COMPLETE: "+$changed+" pages") -ForegroundColor Green
Write-Host "Titles and URLs were preserved; search intent differentiation and related-question links were added." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
