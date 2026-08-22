$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 $bk="_backup_evidence53_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
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
  @((FindBest @("neck-pain.md","*neck*pain*.md","cervical-pain.md") @("\\conditions\\","\\symptoms\\")),"_blocks\neck.md","<!-- MS53_NECK_START -->","<!-- MS53_NECK_END -->","neck pain"),
  @((FindBest @("shoulder-pain.md","*shoulder*pain*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\shoulder.md","<!-- MS53_SHOULDER_START -->","<!-- MS53_SHOULDER_END -->","shoulder pain"),
  @((FindBest @("headache.md","*headache*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\headache.md","<!-- MS53_HEAD_START -->","<!-- MS53_HEAD_END -->","headache"),
  @((FindBest @("dysmenorrhea.md","*dysmenorrhea*.md","menstrual-pain.md") @("\\conditions\\","\\symptoms\\")),"_blocks\dysmenorrhea.md","<!-- MS53_DYSMEN_START -->","<!-- MS53_DYSMEN_END -->","dysmenorrhea")
 )
 $updated=0;$report=@("# 53 Evidence Propagation Report","")
 foreach($i in $items){if($i[0]){if(Patch $i[0] $i[1] $i[2] $i[3]){$updated++;$report+=("- "+$i[4]+": "+$i[0])}}else{$report+=("- "+$i[4]+": SKIP")}}
 New-Item -ItemType Directory -Force "_quality_audit_53"|Out-Null;$report|Set-Content "_quality_audit_53\53_EVIDENCE_PROPAGATION_REPORT.md" -Encoding UTF8
 Write-Host "EVIDENCE PROPAGATION 53 COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"