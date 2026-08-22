$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
try{
 if(!(Test-Path "mkdocs.yml")){throw "mkdocs.yml not found"}
 $bk="mkdocs.yml.backup_67_"+(Get-Date -Format "yyyyMMdd-HHmmss")
 Copy-Item "mkdocs.yml" $bk -Force
 $lines=Get-Content "mkdocs.yml" -Encoding UTF8

 $new=@(
 "          - 과민성장증후군: authority/conditions/irritable-bowel-syndrome.md",
 "          - 기능성 변비: authority/conditions/functional-constipation.md",
 "          - 불안: authority/conditions/anxiety.md",
 "          - 갱년기·주폐경기: authority/conditions/menopause.md",
 "          - 만성전립선염·만성골반통증후군: authority/conditions/chronic-prostatitis-cpps.md",
 "          - 과민성방광: authority/conditions/overactive-bladder.md",
 "          - 천식: authority/conditions/asthma.md",
 "          - COPD: authority/conditions/copd.md",
 "          - 당뇨병성 말초신경병증: authority/conditions/diabetic-peripheral-neuropathy.md",
 "          - 파킨슨병: authority/conditions/parkinson-disease.md",
 "          - 항암치료 유발 오심·구토: authority/conditions/chemotherapy-nausea-vomiting.md",
 "          - 항암치료 유발 말초신경병증: authority/conditions/chemotherapy-induced-peripheral-neuropathy.md",
 "          - 방사선치료 후 구강건조: authority/conditions/radiation-xerostomia.md"
 )
 # Avoid duplicates
 $existing=($lines -join "`n")
 $toAdd=@($new|Where-Object {$existing -notmatch [regex]::Escape(($_ -split ': ',2)[1])})
 if($toAdd.Count -eq 0){
   Write-Host "AUTHORITY MENU FINALIZE 67 COMPLETE" -ForegroundColor Green
   Write-Host "All 13 links already present." -ForegroundColor Cyan
 }else{
   # Find last existing authority/conditions/*.md nav item, insert immediately after it with same indentation.
   $idx=-1
   for($i=0;$i -lt $lines.Count;$i++){
     if($lines[$i] -match 'authority/conditions/.+\.md'){ $idx=$i }
   }
   if($idx -lt 0){throw "No existing authority/conditions nav item found in mkdocs.yml"}
   $before=@($lines[0..$idx])
   $after=if($idx+1 -lt $lines.Count){@($lines[($idx+1)..($lines.Count-1)])}else{@()}
   @($before+$toAdd+$after)|Set-Content "mkdocs.yml" -Encoding UTF8
   Write-Host "AUTHORITY MENU FINALIZE 67 COMPLETE" -ForegroundColor Green
   Write-Host ("Added menu links: "+$toAdd.Count) -ForegroundColor Cyan
 }
}catch{
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"