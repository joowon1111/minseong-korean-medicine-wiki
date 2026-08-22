$ErrorActionPreference="Stop"
function Upsert($f,$s,$e,$b){
 if(-not(Test-Path $f)){return}
 $t=Get-Content $f -Raw -Encoding UTF8
 if($t.Contains($s)){
  $p=[regex]::Escape($s)+".*?"+[regex]::Escape($e)
  $t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)
 }else{$t=$t.TrimEnd()+"`r`n`r`n"+$b+"`r`n"}
 Set-Content $f $t -Encoding UTF8
}
try{
 $R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
 if(-not(Test-Path "docs\diagnostics\patterns\index.md")){throw "15단계 변증 허브가 없습니다."}
 $stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_differential16_"+$stamp
 New-Item -ItemType Directory -Force $bk|Out-Null
 foreach($p in @("docs\diagnostics\index.md","docs\diagnostics\patterns\index.md","docs\clinical-core\index.md","docs\ai-index.md")){
  if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\","_"))) -Force}
 }

 New-Item -ItemType Directory -Force "docs\diagnostics\differentials"|Out-Null
 foreach($x in Get-ChildItem "_payload\differentials" -File){
  Copy-Item $x.FullName (Join-Path "docs\diagnostics\differentials" $x.Name) -Force
 }

 $diag=@'
<!-- DIFFERENTIAL_NETWORK_16_START -->
## 임상 변증 감별
비슷한 증상에서 **어느 변증에 더 무게를 둘지** 비교합니다.

- [기허·혈허·기혈양허](differentials/qi-vs-blood-vs-qi-blood.md)
- [담음·식적](differentials/phlegm-vs-food-stagnation.md)
- [어혈·한습성 통증](differentials/blood-stasis-vs-cold-damp-pain.md)
- [간울·담음성 흉민](differentials/liver-qi-vs-phlegm-chest.md)
- [신음허·신양허](differentials/kidney-yin-vs-yang.md)
- [기허·신허성 피로](differentials/qi-deficiency-vs-kidney-deficiency-fatigue.md)

→ [임상 변증 감별 전체 보기](differentials/index.md)
<!-- DIFFERENTIAL_NETWORK_16_END -->
'@
 Upsert "docs\diagnostics\index.md" "<!-- DIFFERENTIAL_NETWORK_16_START -->" "<!-- DIFFERENTIAL_NETWORK_16_END -->" $diag

 $patterns=@'
<!-- DIFFERENTIAL_FROM_PATTERNS_16_START -->
## 비슷한 변증 비교하기
- [임상 변증 감별 지도](../differentials/index.md)
<!-- DIFFERENTIAL_FROM_PATTERNS_16_END -->
'@
 Upsert "docs\diagnostics\patterns\index.md" "<!-- DIFFERENTIAL_FROM_PATTERNS_16_START -->" "<!-- DIFFERENTIAL_FROM_PATTERNS_16_END -->" $patterns

 $clinical=@'
<!-- DIFFERENTIAL_CLINICAL_CORE_16_START -->
## 변증을 서로 비교하기
증상별 임상 경로에서 한 단계 더 들어가 **기허·혈허, 담음·식적, 어혈·한습, 신음허·신양허** 등을 비교합니다.

→ [임상 변증 감별 지도](../diagnostics/differentials/index.md)
<!-- DIFFERENTIAL_CLINICAL_CORE_16_END -->
'@
 Upsert "docs\clinical-core\index.md" "<!-- DIFFERENTIAL_CLINICAL_CORE_16_START -->" "<!-- DIFFERENTIAL_CLINICAL_CORE_16_END -->" $clinical

 $ai=@'
<!-- DIFFERENTIAL_AI_16_START -->
## 변증 감별로 찾기
- [기허·혈허·기혈양허](diagnostics/differentials/qi-vs-blood-vs-qi-blood.md)
- [담음·식적](diagnostics/differentials/phlegm-vs-food-stagnation.md)
- [어혈·한습성 통증](diagnostics/differentials/blood-stasis-vs-cold-damp-pain.md)
- [신음허·신양허](diagnostics/differentials/kidney-yin-vs-yang.md)
<!-- DIFFERENTIAL_AI_16_END -->
'@
 Upsert "docs\ai-index.md" "<!-- DIFFERENTIAL_AI_16_START -->" "<!-- DIFFERENTIAL_AI_16_END -->" $ai

 Write-Host "PATTERN DIFFERENTIAL EXPANSION 16 COMPLETE" -ForegroundColor Green
 Write-Host "6 clinical differential maps integrated into diagnostics and clinical-core." -ForegroundColor Green
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
