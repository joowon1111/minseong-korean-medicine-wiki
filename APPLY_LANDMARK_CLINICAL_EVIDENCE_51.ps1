$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
try{
 if(!(Test-Path "docs\research\references.md")){throw "docs\research\references.md not found"}
 $bk="_backup_landmark_evidence51_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
 function Patch($target,$blockfile,$start,$end,$before){
  if(!(Test-Path $target)){Write-Host ("SKIP "+$target) -ForegroundColor DarkYellow;return}
  $txt=Get-Content $target -Raw -Encoding UTF8;$block=Get-Content $blockfile -Raw -Encoding UTF8
  Copy-Item $target (Join-Path $bk ($target.Replace("\","_"))) -Force
  $pat='(?s)'+[regex]::Escape($start)+'.*?'+[regex]::Escape($end)
  if($txt -match $pat){$txt=[regex]::Replace($txt,$pat,[System.Text.RegularExpressions.MatchEvaluator]{param($m)$block})}
  elseif($before -and $txt -match $before){$m=[regex]::Match($txt,$before);$txt=$txt.Insert($m.Index,$block+"`r`n`r`n")}
  else{$txt+="`r`n`r`n"+$block}
  Set-Content $target $txt -Encoding UTF8
 }
 Patch "docs\research\references.md" "_blocks\refs.md" "<!-- MS51_REFS_START -->" "<!-- MS51_REFS_END -->" "(?m)^##\s+활용 방법"
 Patch "docs\evidence-integrated\acupuncture-evidence.md" "_blocks\acu.md" "<!-- MS51_ACU_START -->" "<!-- MS51_ACU_END -->" "(?m)^##\s+관련"
 Patch "docs\treatments\electroacupuncture.md" "_blocks\ea.md" "<!-- MS51_EA_START -->" "<!-- MS51_EA_END -->" "(?m)^##\s+관련"
 Patch "docs\treatments\pharmacopuncture.md" "_blocks\pharm.md" "<!-- MS51_PHARM_START -->" "<!-- MS51_PHARM_END -->" "(?m)^##\s+관련"
 Patch "docs\evidence-integrated\herbal-evidence.md" "_blocks\herb.md" "<!-- MS51_HERB_START -->" "<!-- MS51_HERB_END -->" "(?m)^##\s+표현 원칙"
 Patch "docs\conditions\low-back-pain.md" "_blocks\lbp.md" "<!-- MS51_LBP_START -->" "<!-- MS51_LBP_END -->" "(?m)^##\s+관련"
 Patch "docs\conditions\knee-pain.md" "_blocks\knee.md" "<!-- MS51_KNEE_START -->" "<!-- MS51_KNEE_END -->" "(?m)^##\s+관련"
 Patch "docs\conditions\rhinitis.md" "_blocks\rhinitis.md" "<!-- MS51_RHIN_START -->" "<!-- MS51_RHIN_END -->" "(?m)^##\s+관련"
 Write-Host "LANDMARK CLINICAL EVIDENCE 51 COMPLETE" -ForegroundColor Green
 Write-Host "Reference database and existing treatment/condition evidence pages updated." -ForegroundColor Cyan
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"