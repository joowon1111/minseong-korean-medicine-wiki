$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
$Out=Join-Path $R "_quality_audit_37"
New-Item -ItemType Directory -Force $Out|Out-Null
$Progress=Join-Path $Out "AUDIT_PROGRESS.txt"
$ErrorFile=Join-Path $Out "AUDIT_ERROR_FULL.txt"
try{
 "STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"|Set-Content $Progress -Encoding UTF8
 if(!(Test-Path "docs")){throw "docs not found"}
 $rows=@()
 $files=@(Get-ChildItem "docs" -Recurse -Filter *.md -File)
 $i=0
 foreach($f in $files){
  $i++
  if(($i%100)-eq 0){Write-Host ("SCANNING "+$i+" / "+$files.Count) -ForegroundColor Yellow}
  $txt=Get-Content $f.FullName -Raw -Encoding UTF8
  if($null -eq $txt){$txt=""}
  $rel=$f.FullName.Substring((Resolve-Path "docs").Path.Length+1).Replace("\","/")
  $body=$txt -replace '(?s)^---\s*.*?\s*---\s*',''
  $chars=($body -replace '\s+','').Length
  $heads=([regex]::Matches($body,'(?m)^#{1,6}\s+')).Count
  $links=([regex]::Matches($body,'\[[^\]]+\]\((?!https?://|#)([^)]+)\)')).Count
  $kind="content"
  if($rel.StartsWith("templates/")){$kind="template"}
  elseif($rel.EndsWith("/references.md") -or $rel -eq "references.md"){$kind="references"}
  elseif($txt -match '(?m)^status\s*:\s*canonical-bridge\s*$'){$kind="bridge"}
  $score=0;$reason=@()
  if($kind -eq "content"){
   if($chars -lt 500){$score+=5;$reason+="very short"}
   elseif($chars -lt 900){$score+=3;$reason+="short"}
   if($heads -lt 3){$score+=2;$reason+="few sections"}
   if($links -lt 2){$score+=2;$reason+="few links"}
  }
  $rows += [PSCustomObject]@{score=$score;kind=$kind;path=$rel;body_chars=$chars;headings=$heads;internal_links=$links;reasons=($reason -join "; ")}
 }
 $sorted=@($rows|Sort-Object @{Expression="score";Descending=$true},path)
 $sorted|Export-Csv (Join-Path $Out "AUDIT_RANKING_37.tsv") -Delimiter "`t" -NoTypeInformation -Encoding UTF8
 $priority=@($sorted|Where-Object {$_.kind -eq "content" -and $_.score -ge 5})
 $excluded=@($sorted|Where-Object {$_.kind -ne "content"})
 $report=@("# Quality Audit 37 — duplicate-aware","",
 "- Markdown: **$($sorted.Count)**",
 "- True content priority candidates: **$($priority.Count)**",
 "- Bridge/template/reference excluded from ordinary length scoring: **$($excluded.Count)**","",
 "## Top true-content candidates","")
 foreach($x in ($priority|Select-Object -First 100)){
  $report += "- ``$($x.path)`` — score $($x.score), $($x.body_chars) chars, $($x.reasons)"
 }
 $report|Set-Content (Join-Path $Out "AUDIT_REPORT_37.md") -Encoding UTF8
 @("COMPLETE","Markdown: $($sorted.Count)","Priority: $($priority.Count)","Excluded special-purpose pages: $($excluded.Count)")|Set-Content $Progress -Encoding UTF8
 ""|Set-Content $ErrorFile -Encoding UTF8
 Write-Host "DUPLICATE-AWARE QUALITY AUDIT 37 FIXED COMPLETE" -ForegroundColor Green
 Write-Host "Created _quality_audit_37\AUDIT_REPORT_37.md and AUDIT_RANKING_37.tsv" -ForegroundColor Cyan
}catch{
 ($_|Out-String)|Set-Content $ErrorFile -Encoding UTF8
 "FAILED"|Set-Content $Progress -Encoding UTF8
 Write-Host ("AUDIT ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
