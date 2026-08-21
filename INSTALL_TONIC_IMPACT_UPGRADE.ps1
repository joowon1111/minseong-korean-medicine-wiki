$ErrorActionPreference="Stop"
function Upsert($file,$s,$e,$block){
 if(-not(Test-Path $file)){return}
 $t=Get-Content $file -Raw -Encoding UTF8
 if($t.Contains($s)){
  $pat=[regex]::Escape($s)+".*?"+[regex]::Escape($e)
  $t=[regex]::Replace($t,$pat,$block,[Text.RegularExpressions.RegexOptions]::Singleline)
 } else {$t=$t.TrimEnd()+"`r`n`r`n"+$block+"`r`n"}
 Set-Content $file $t -Encoding UTF8
}
try{
 $R=Split-Path -Parent $MyInvocation.MyCommand.Path; Set-Location $R
 if(-not(Test-Path "docs")){throw "docs folder not found"}
 $stamp=Get-Date -Format "yyyyMMdd-HHmmss"; $bk="_backup_tonic_impact_"+$stamp
 New-Item -ItemType Directory -Force $bk|Out-Null
 foreach($p in @("docs\\clinical-guides","docs\\pillar\\tonic-recovery.md","docs\\herbs\\cervi-parvum-cornu.md","docs\\formulas\\index.md","docs\\ai-index.md")){
  if(Test-Path $p){Copy-Item $p (Join-Path $bk ([IO.Path]::GetFileName($p))) -Recurse -Force}
 }
 New-Item -ItemType Directory -Force "docs\\clinical-guides"|Out-Null
 Copy-Item "_tonic_impact_payload\\*.md" "docs\\clinical-guides\\" -Force

 $hero=@'
<!-- TONIC_IMPACT_START -->

## 보약·녹용보약 핵심 탐색

보약은 처방명만 고르는 것이 아니라 **현재 증상 → 회복 단계 → 처방 구조 → 약재 품질 → 용량·제형 → 현대 연구**까지 함께 보는 것이 핵심입니다.

- [어떤 보약을 선택해야 하나요? — 증상별 처방 지도](../clinical-guides/tonic-decision-map.md)
- [녹용의 품질은 무엇으로 판단하나요?](../clinical-guides/deer-antler-quality-map.md)
- [대표 보약 처방 비교표](../clinical-guides/tonic-comparison-matrix.md)
- [보익 처방 현대 연구 대시보드](../clinical-guides/tonic-evidence-dashboard.md)
- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)
- [보약 처방의 용량·출전·품질](../clinical-guides/tonic-formula-dose-source-quality.md)

<!-- TONIC_IMPACT_END -->
'@
 Upsert "docs\\pillar\\tonic-recovery.md" "<!-- TONIC_IMPACT_START -->" "<!-- TONIC_IMPACT_END -->" $hero

 $deer=@'
<!-- DEER_IMPACT_START -->

## 녹용을 더 입체적으로 보기

- [녹용의 품질은 무엇으로 판단하나요? — 부위·조직·가공·유통](../clinical-guides/deer-antler-quality-map.md)
- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)
- [어떤 보약을 선택해야 하나요?](../clinical-guides/tonic-decision-map.md)
- [대표 보약 처방 비교표](../clinical-guides/tonic-comparison-matrix.md)

<!-- DEER_IMPACT_END -->
'@
 Upsert "docs\\herbs\\cervi-parvum-cornu.md" "<!-- DEER_IMPACT_START -->" "<!-- DEER_IMPACT_END -->" $deer

 $f=@'
<!-- FORMULA_IMPACT_START -->

## 보약 처방 비교·선택

- [대표 보약 처방 비교표](../clinical-guides/tonic-comparison-matrix.md)
- [어떤 보약을 선택해야 하나요?](../clinical-guides/tonic-decision-map.md)
- [보약 처방의 용량·출전·품질](../clinical-guides/tonic-formula-dose-source-quality.md)
- [보익 처방 현대 연구 대시보드](../clinical-guides/tonic-evidence-dashboard.md)

<!-- FORMULA_IMPACT_END -->
'@
 Upsert "docs\\formulas\\index.md" "<!-- FORMULA_IMPACT_START -->" "<!-- FORMULA_IMPACT_END -->" $f

 $ai=@'
<!-- TONIC_AI_IMPACT_START -->

## 보약·녹용보약 빠른 가이드

- [어떤 보약을 선택해야 하나요?](clinical-guides/tonic-decision-map.md)
- [녹용의 품질은 무엇으로 판단하나요?](clinical-guides/deer-antler-quality-map.md)
- [대표 보약 처방 비교표](clinical-guides/tonic-comparison-matrix.md)
- [보익 처방 현대 연구 대시보드](clinical-guides/tonic-evidence-dashboard.md)

<!-- TONIC_AI_IMPACT_END -->
'@
 Upsert "docs\\ai-index.md" "<!-- TONIC_AI_IMPACT_START -->" "<!-- TONIC_AI_IMPACT_END -->" $ai

 Write-Host "TONIC IMPACT UPGRADE COMPLETE" -ForegroundColor Green
 Write-Host "4 new deep guides created and linked." -ForegroundColor Green
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
