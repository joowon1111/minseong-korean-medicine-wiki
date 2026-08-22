$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 $bk="_backup_oncology64_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
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
  @((FindBest @("*chemotherapy*nausea*.md","*cinv*.md","*nausea*vomit*.md") @("\\conditions\\","\\cancer","\\oncology","\\support")),"_blocks\cinv.md","<!-- MS64_CINV_START -->","<!-- MS64_CINV_END -->","CINV"),
  @((FindBest @("*chemotherapy*neuropathy*.md","*cipn*.md") @("\\conditions\\","\\cancer","\\oncology","\\neuro")),"_blocks\cipn.md","<!-- MS64_CIPN_START -->","<!-- MS64_CIPN_END -->","CIPN"),
  @((FindBest @("*xerostomia*.md","*dry*mouth*.md") @("\\conditions\\","\\cancer","\\oncology","\\symptoms")),"_blocks\xerostomia.md","<!-- MS64_XERO_START -->","<!-- MS64_XERO_END -->","xerostomia"),
  @((FindBest @("*cancer*.md","*oncology*.md","*supportive*.md") @("\\pillar\\","\\conditions\\","\\support")),"_blocks\oncologyhub.md","<!-- MS64_ONC_START -->","<!-- MS64_ONC_END -->","oncology supportive hub")
 )
 $updated=0;$report=@("# 64 Oncology Supportive Evidence Report","")
 foreach($i in $items){if($i[0]){if(Patch $i[0] $i[1] $i[2] $i[3]){$updated++;$report+=("- "+$i[4]+": "+$i[0])}}else{$report+=("- "+$i[4]+": SKIP")}}
 New-Item -ItemType Directory -Force "_quality_audit_64"|Out-Null;$report|Set-Content "_quality_audit_64\64_ONCOLOGY_EVIDENCE_REPORT.md" -Encoding UTF8
 Write-Host "ONCOLOGY SUPPORTIVE EVIDENCE PROPAGATION 64 COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"