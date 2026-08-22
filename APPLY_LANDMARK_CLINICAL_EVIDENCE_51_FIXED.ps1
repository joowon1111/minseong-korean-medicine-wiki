$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
try{
 if(!(Test-Path "docs")){throw "docs not found"}
 if(!(Test-Path "mkdocs.yml")){throw "mkdocs.yml not found"}

 $bk="_backup_landmark_evidence51_fixed_"+(Get-Date -Format "yyyyMMdd-HHmmss")
 New-Item -ItemType Directory -Force $bk|Out-Null

 $cfg=Get-Content "mkdocs.yml" -Raw -Encoding UTF8
 $matches=[regex]::Matches($cfg,'(?im)^\s*-\s*[^:\r\n]*references[^:\r\n]*:\s*([^\r\n#]+\.md)\s*$')
 $refRel=$null
 foreach($m in $matches){
   $candidate=$m.Groups[1].Value.Trim().Trim('"').Trim("'")
   if(Test-Path (Join-Path "docs" $candidate)){
     if($candidate -match '(^|/)research(/|-)'){ $refRel=$candidate;break }
     if(!$refRel){$refRel=$candidate}
   }
 }
 if(!$refRel){
   $all=Get-ChildItem "docs" -Recurse -File -Filter "references.md"
   foreach($f in $all){
     $rel=$f.FullName.Substring((Resolve-Path "docs").Path.Length+1).Replace("\","/")
     if($rel -match 'research'){ $refRel=$rel;break }
   }
 }
 if(!$refRel){throw "Could not identify canonical references.md"}

 $refTarget=Join-Path "docs" $refRel
 Write-Host ("Canonical references: "+$refTarget) -ForegroundColor Cyan

 function Patch($target,$blockfile,$start,$end){
   if(!(Test-Path $target)){Write-Host ("SKIP missing: "+$target) -ForegroundColor DarkYellow;return $false}
   $txt=Get-Content $target -Raw -Encoding UTF8
   $block=Get-Content $blockfile -Raw -Encoding UTF8
   Copy-Item $target (Join-Path $bk ($target.Replace("\","_").Replace("/","_"))) -Force
   $pat='(?s)'+[regex]::Escape($start)+'.*?'+[regex]::Escape($end)
   if($txt -match $pat){$txt=[regex]::Replace($txt,$pat,[System.Text.RegularExpressions.MatchEvaluator]{param($m)$block})}
   else{$txt+="`r`n`r`n"+$block+"`r`n"}
   Set-Content $target $txt -Encoding UTF8
   return $true
 }

 $updated=0
 if(Patch $refTarget "_blocks\refs.md" "<!-- MS51_REFS_START -->" "<!-- MS51_REFS_END -->"){$updated++}

 # Search candidate files by basename/semantic folder rather than assuming one fixed path.
 function FirstExisting([string[]]$patterns){
   foreach($p in $patterns){
     $x=Get-ChildItem "docs" -Recurse -File -Filter $p | Where-Object {$_.FullName -notmatch '_AUDIT|_backup|_payload'} | Select-Object -First 1
     if($x){return $x.FullName}
   }
   return $null
 }

 $targets=@(
   @((FirstExisting @("acupuncture-evidence.md")),"_blocks\acu.md","<!-- MS51_ACU_START -->","<!-- MS51_ACU_END -->"),
   @((FirstExisting @("electroacupuncture.md")),"_blocks\ea.md","<!-- MS51_EA_START -->","<!-- MS51_EA_END -->"),
   @((FirstExisting @("pharmacopuncture.md")),"_blocks\pharm.md","<!-- MS51_PHARM_START -->","<!-- MS51_PHARM_END -->"),
   @((FirstExisting @("herbal-evidence.md")),"_blocks\herb.md","<!-- MS51_HERB_START -->","<!-- MS51_HERB_END -->"),
   @((FirstExisting @("low-back-pain.md","low-back*.md")),"_blocks\lbp.md","<!-- MS51_LBP_START -->","<!-- MS51_LBP_END -->"),
   @((FirstExisting @("knee-pain.md","knee*.md")),"_blocks\knee.md","<!-- MS51_KNEE_START -->","<!-- MS51_KNEE_END -->"),
   @((FirstExisting @("rhinitis.md","*rhinitis*.md")),"_blocks\rhinitis.md","<!-- MS51_RHIN_START -->","<!-- MS51_RHIN_END -->")
 )
 foreach($t in $targets){
   if($t[0]){if(Patch $t[0] $t[1] $t[2] $t[3]){$updated++}}
 }

 @(
  "COMPLETE",
  ("Canonical references: "+$refRel),
  ("Updated files: "+$updated),
  ("Backup: "+$bk)
 )|Set-Content "APPLY_51_FIXED_STATUS.txt" -Encoding UTF8

 Write-Host "LANDMARK CLINICAL EVIDENCE 51 FIXED COMPLETE" -ForegroundColor Green
 Write-Host ("Updated files: "+$updated) -ForegroundColor Cyan
 Write-Host ("References: "+$refRel) -ForegroundColor Yellow
}catch{
 ("FAILED`r`n"+($_|Out-String))|Set-Content "APPLY_51_FIXED_STATUS.txt" -Encoding UTF8
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
 Write-Host "See APPLY_51_FIXED_STATUS.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"