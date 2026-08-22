$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 $bk="_backup_evidence61_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
 function FindBest([string[]]$names,[string[]]$prefer){
  $all=@();foreach($n in $names){$all+=@(Get-ChildItem "docs" -Recurse -File -Filter $n|Where-Object {$_.FullName -notmatch '_AUDIT|_backup|_payload'})}
  $all=@($all|Sort-Object FullName -Unique);if(!$all.Count){return $null}
  foreach($p in $prefer){$x=$all|Where-Object {$_.FullName -match $p}|Select-Object -First 1;if($x){return $x.FullName}}
  return $all[0].FullName
 }
 function Patch($target,$blockfile,$start,$end){
  if(!$target){return $false};$txt=Get-Content $target -Raw -Encoding UTF8;$block=Get-Content $blockfile -Raw -Encoding UTF8
  Copy-Item $target (Join-Path $bk ($target.Replace("\","_").Replace(":",""))) -Force
  $pat='(?s)'+[regex]::Escape($start)+'.*?'+[regex]::Escape($end)
  if($txt -match $pat){$txt=[regex]::Replace($txt,$pat,[System.Text.RegularExpressions.MatchEvaluator]{param($m)$block})}else{$txt+="`r`n`r`n"+$block}
  Set-Content $target $txt -Encoding UTF8;return $true
 }
 $items=@(
  @((FindBest @("*diabetic*neuropathy*.md","*peripheral*neuropathy*.md","*neuropathy*.md") @("\\conditions\\","\\symptoms\\","\\neuro")),"_blocks\dPN.md","<!-- MS61_DPN_START -->","<!-- MS61_DPN_END -->","diabetic peripheral neuropathy"),
  @((FindBest @("*fibromyalgia*.md") @("\\conditions\\","\\pain","\\symptoms\\")),"_blocks\fibro.md","<!-- MS61_FIBRO_START -->","<!-- MS61_FIBRO_END -->","fibromyalgia"),
  @((FindBest @("*shoulder*hand*.md","*post*stroke*shoulder*.md") @("\\conditions\\","\\neuro","\\rehab")),"_blocks\poststroke.md","<!-- MS61_SHS_START -->","<!-- MS61_SHS_END -->","post-stroke shoulder-hand syndrome")
 )
 $updated=0;$report=@("# 61 Neuropathic and Fibromyalgia Evidence Report","")
 foreach($i in $items){if($i[0]){if(Patch $i[0] $i[1] $i[2] $i[3]){$updated++;$report+=("- "+$i[4]+": "+$i[0])}}else{$report+=("- "+$i[4]+": SKIP")}}
 New-Item -ItemType Directory -Force "_quality_audit_61"|Out-Null;$report|Set-Content "_quality_audit_61\61_EVIDENCE_REPORT.md" -Encoding UTF8
 Write-Host "NEUROPATHIC FIBROMYALGIA EVIDENCE 61 COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"