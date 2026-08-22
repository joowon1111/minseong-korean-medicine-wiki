$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 $bk="_backup_evidence55_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
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
  @((FindBest @("fatigue.md","*chronic*fatigue*.md") @("\\conditions\\","\\symptoms\\","\\autonomic\\")),"_blocks\fatigue.md","<!-- MS55_FATIGUE_START -->","<!-- MS55_FATIGUE_END -->","fatigue"),
  @((FindBest @("anxiety.md","*anxiety*.md") @("\\conditions\\","\\symptoms\\","\\autonomic\\")),"_blocks\anxiety.md","<!-- MS55_ANXIETY_START -->","<!-- MS55_ANXIETY_END -->","anxiety"),
  @((FindBest @("*hypogalactia*.md","*lactation*.md","*postpartum*.md") @("\\conditions\\","\\women","\\gyne","\\postpartum")),"_blocks\postpartum-lactation.md","<!-- MS55_POSTPARTUM_START -->","<!-- MS55_POSTPARTUM_END -->","postpartum lactation"),
  @((FindBest @("*cancer*.md","*oncology*.md","*aromatase*.md") @("\\conditions\\","\\support","\\cancer")),"_blocks\cancer-support.md","<!-- MS55_CANCER_START -->","<!-- MS55_CANCER_END -->","cancer supportive care")
 )
 $updated=0;$report=@("# 55 Evidence Propagation Report","")
 foreach($i in $items){if($i[0]){if(Patch $i[0] $i[1] $i[2] $i[3]){$updated++;$report+=("- "+$i[4]+": "+$i[0])}}else{$report+=("- "+$i[4]+": SKIP")}}
 New-Item -ItemType Directory -Force "_quality_audit_55"|Out-Null;$report|Set-Content "_quality_audit_55\55_EVIDENCE_PROPAGATION_REPORT.md" -Encoding UTF8
 Write-Host "EVIDENCE PROPAGATION 55 COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"