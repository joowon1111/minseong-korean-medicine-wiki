$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 $bk="_backup_evidence52_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null

 function FindBest([string[]]$names,[string[]]$prefer){
   $all=@()
   foreach($name in $names){
     $all += @(Get-ChildItem "docs" -Recurse -File -Filter $name | Where-Object {$_.FullName -notmatch '_AUDIT|_backup|_payload'})
   }
   $all=@($all|Sort-Object FullName -Unique)
   if($all.Count -eq 0){return $null}
   foreach($p in $prefer){
     $hit=$all|Where-Object {$_.FullName -match $p}|Select-Object -First 1
     if($hit){return $hit.FullName}
   }
   return $all[0].FullName
 }

 function Patch($target,$blockfile,$start,$end){
   if(!$target -or !(Test-Path $target)){return $false}
   $txt=Get-Content $target -Raw -Encoding UTF8;$block=Get-Content $blockfile -Raw -Encoding UTF8
   Copy-Item $target (Join-Path $bk ($target.Replace("\","_").Replace(":",""))) -Force
   $pat='(?s)'+[regex]::Escape($start)+'.*?'+[regex]::Escape($end)
   if($txt -match $pat){$txt=[regex]::Replace($txt,$pat,[System.Text.RegularExpressions.MatchEvaluator]{param($m)$block})}
   else{$txt+="`r`n`r`n"+$block}
   Set-Content $target $txt -Encoding UTF8
   return $true
 }

 $items=@(
  @((FindBest @("low-back-pain.md","low-back*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\lbp.md","<!-- MS52_LBP_START -->","<!-- MS52_LBP_END -->","low back pain"),
  @((FindBest @("knee-pain.md","knee*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\knee.md","<!-- MS52_KNEE_START -->","<!-- MS52_KNEE_END -->","knee"),
  @((FindBest @("dyspepsia.md","*dyspepsia*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\dyspepsia.md","<!-- MS52_DYS_START -->","<!-- MS52_DYS_END -->","dyspepsia"),
  @((FindBest @("insomnia.md","*insomnia*.md") @("\\conditions\\","\\symptoms\\")),"_blocks\insomnia.md","<!-- MS52_INS_START -->","<!-- MS52_INS_END -->","insomnia"),
  @((FindBest @("pharmacopuncture.md","*pharmacopuncture*.md") @("\\treatments\\","\\acupuncture")),"_blocks\pharm.md","<!-- MS52_PHARM_START -->","<!-- MS52_PHARM_END -->","pharmacopuncture")
 )
 $updated=0;$report=@("# 52 Evidence Propagation Report","")
 foreach($i in $items){
   if($i[0]){
     if(Patch $i[0] $i[1] $i[2] $i[3]){$updated++;$report+=("- "+$i[4]+": "+$i[0])}
   }else{$report+=("- "+$i[4]+": SKIP (file not found)")}
 }
 New-Item -ItemType Directory -Force "_quality_audit_52"|Out-Null
 $report|Set-Content "_quality_audit_52\52_EVIDENCE_PROPAGATION_REPORT.md" -Encoding UTF8
 Write-Host "EVIDENCE PROPAGATION 52 COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host "Landmark studies paired with newer systematic reviews/meta-analyses." -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"