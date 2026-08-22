$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R

try{
 if(!(Test-Path "docs")){throw "docs not found"}
 if(!(Test-Path "mkdocs.yml")){throw "mkdocs.yml not found"}

 $bk="_backup_landmark_evidence51_v2_"+(Get-Date -Format "yyyyMMdd-HHmmss")
 New-Item -ItemType Directory -Force $bk|Out-Null

 $lines=Get-Content "mkdocs.yml" -Encoding UTF8
 $candidates=@()

 foreach($line in $lines){
   # Match nav targets ending in references.md; label may be Korean.
   $m=[regex]::Match($line,':\s*["'']?([^#\r\n]+references\.md)["'']?\s*$',[System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
   if($m.Success){
     $rel=$m.Groups[1].Value.Trim().Trim('"').Trim("'")
     $full=Join-Path "docs" $rel
     if(Test-Path $full){
       $score=0
       if($rel -match '(?i)research'){ $score+=100 }
       if($line -match '연구|근거|참고문헌'){ $score+=50 }
       $candidates += [PSCustomObject]@{Rel=$rel;Full=$full;Score=$score;Line=$line}
     }
   }
 }

 # If nav did not expose it, rank all docs/**/references.md.
 if($candidates.Count -eq 0){
   foreach($f in Get-ChildItem "docs" -Recurse -File -Filter "references.md"){
     if($f.FullName -match '_AUDIT|_backup|_payload'){continue}
     $rel=$f.FullName.Substring((Resolve-Path "docs").Path.Length+1).Replace("\","/")
     $score=0
     if($rel -match '(?i)research'){ $score+=100 }
     $txt=Get-Content $f.FullName -Raw -Encoding UTF8
     if($txt -match '침|약침|한약|임상|연구|PMID|DOI|근거'){ $score+=20 }
     $candidates += [PSCustomObject]@{Rel=$rel;Full=$f.FullName;Score=$score;Line=""}
   }
 }

 if($candidates.Count -eq 0){throw "No references.md found under docs"}

 $chosen=$candidates | Sort-Object Score -Descending | Select-Object -First 1
 $refTarget=$chosen.Full
 Write-Host ("Chosen references: "+$chosen.Rel) -ForegroundColor Cyan

 function PatchFile([string]$target,[string]$blockfile,[string]$start,[string]$end){
   if(!(Test-Path $target)){return $false}
   $txt=Get-Content $target -Raw -Encoding UTF8
   $block=Get-Content $blockfile -Raw -Encoding UTF8
   Copy-Item $target (Join-Path $bk ($target.Replace("\","_").Replace("/","_").Replace(":",""))) -Force
   $pat='(?s)'+[regex]::Escape($start)+'.*?'+[regex]::Escape($end)
   if($txt -match $pat){
     $txt=[regex]::Replace($txt,$pat,[System.Text.RegularExpressions.MatchEvaluator]{param($m)$block})
   }else{
     $txt+="`r`n`r`n"+$block+"`r`n"
   }
   Set-Content $target $txt -Encoding UTF8
   return $true
 }

 $updated=0
 if(PatchFile $refTarget "_blocks\refs.md" "<!-- MS51_REFS_START -->" "<!-- MS51_REFS_END -->"){$updated++}

 # Related pages: only patch the first real docs file with the exact basename.
 $related=@(
  @("acupuncture-evidence.md","_blocks\acu.md","<!-- MS51_ACU_START -->","<!-- MS51_ACU_END -->"),
  @("electroacupuncture.md","_blocks\ea.md","<!-- MS51_EA_START -->","<!-- MS51_EA_END -->"),
  @("pharmacopuncture.md","_blocks\pharm.md","<!-- MS51_PHARM_START -->","<!-- MS51_PHARM_END -->"),
  @("herbal-evidence.md","_blocks\herb.md","<!-- MS51_HERB_START -->","<!-- MS51_HERB_END -->")
 )
 foreach($r in $related){
   $f=Get-ChildItem "docs" -Recurse -File -Filter $r[0] | Where-Object {$_.FullName -notmatch '_AUDIT|_backup|_payload'} | Select-Object -First 1
   if($f){
     if(PatchFile $f.FullName $r[1] $r[2] $r[3]){$updated++}
   }
 }

 # Write diagnostic list of all candidate reference paths for transparency.
 $diag=@("# 51 references path selection","",("Chosen: **"+$chosen.Rel+"**"),"","## Candidates")
 foreach($c in ($candidates|Sort-Object Score -Descending)){
   $diag+=("- "+$c.Rel+" (score "+$c.Score+")")
 }
 New-Item -ItemType Directory -Force "_quality_audit_51"|Out-Null
 $diag|Set-Content "_quality_audit_51\51_REFERENCE_PATH_REPORT.md" -Encoding UTF8

 @(
   "COMPLETE",
   ("Chosen references: "+$chosen.Rel),
   ("Updated files: "+$updated),
   "Report: _quality_audit_51/51_REFERENCE_PATH_REPORT.md",
   ("Backup: "+$bk)
 )|Set-Content "APPLY_51_FIXED_V2_STATUS.txt" -Encoding UTF8

 Write-Host "LANDMARK CLINICAL EVIDENCE 51 FIXED V2 COMPLETE" -ForegroundColor Green
 Write-Host ("Chosen references: "+$chosen.Rel) -ForegroundColor Yellow
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
}catch{
 ("FAILED`r`n"+($_|Out-String))|Set-Content "APPLY_51_FIXED_V2_STATUS.txt" -Encoding UTF8
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
 Write-Host "See APPLY_51_FIXED_V2_STATUS.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"