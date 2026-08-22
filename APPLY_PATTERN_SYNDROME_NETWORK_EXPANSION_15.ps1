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
 if(-not(Test-Path "docs\diagnostics\index.md")){throw "docs\diagnostics\index.md not found"}
 $stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_patterns15_"+$stamp
 New-Item -ItemType Directory -Force $bk|Out-Null

 foreach($p in @("docs\diagnostics\index.md","docs\foundations\index.md","docs\network\index.md","docs\clinical-core\index.md","docs\ai-index.md")){
  if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\","_"))) -Force}
 }

 New-Item -ItemType Directory -Force "docs\diagnostics\patterns"|Out-Null
 foreach($x in Get-ChildItem "_payload\patterns" -File){
  Copy-Item $x.FullName (Join-Path "docs\diagnostics\patterns" $x.Name) -Force
 }

 $diag=@'
<!-- PATTERN_NETWORK_15_START -->
## 임상 핵심 변증
기허·혈허·기혈양허·담음·어혈·한습·간울·신허를 **증상 → 설·맥 참고점 → 본초 → 방제 → 경혈 → 환자 질문 → 현대 연구**로 연결합니다.

→ [임상 핵심 변증 지도](patterns/index.md)
<!-- PATTERN_NETWORK_15_END -->
'@
 Upsert "docs\diagnostics\index.md" "<!-- PATTERN_NETWORK_15_START -->" "<!-- PATTERN_NETWORK_15_END -->" $diag

 $foundation=@'
<!-- PATTERN_FOUNDATION_15_START -->
## 기혈진액에서 임상 변증으로
기·혈·진액의 기초 개념을 실제 임상 변증과 연결해 볼 수 있습니다.

→ [임상 핵심 변증 지도](../diagnostics/patterns/index.md)
<!-- PATTERN_FOUNDATION_15_END -->
'@
 Upsert "docs\foundations\index.md" "<!-- PATTERN_FOUNDATION_15_START -->" "<!-- PATTERN_FOUNDATION_15_END -->" $foundation

 $network=@'
<!-- PATTERN_KNOWLEDGE_NETWORK_15_START -->
## 변증에서 본초·방제·경혈로
- [임상 핵심 변증 지도](../diagnostics/patterns/index.md)
<!-- PATTERN_KNOWLEDGE_NETWORK_15_END -->
'@
 Upsert "docs\network\index.md" "<!-- PATTERN_KNOWLEDGE_NETWORK_15_START -->" "<!-- PATTERN_KNOWLEDGE_NETWORK_15_END -->" $network

 $clinical=@'
<!-- PATTERN_CLINICAL_CORE_15_START -->
## 변증을 중심으로 다시 보기
임상 증상별 경로와 본초·방제·경혈 조합을 **기허·혈허·담음·어혈·한습·간울·신허** 등 변증 관점에서 다시 연결합니다.

→ [임상 핵심 변증 지도](../diagnostics/patterns/index.md)
<!-- PATTERN_CLINICAL_CORE_15_END -->
'@
 Upsert "docs\clinical-core\index.md" "<!-- PATTERN_CLINICAL_CORE_15_START -->" "<!-- PATTERN_CLINICAL_CORE_15_END -->" $clinical

 $ai=@'
<!-- PATTERN_AI_INDEX_15_START -->
## 변증으로 찾기
- [임상 핵심 변증 지도](diagnostics/patterns/index.md)
- [기허](diagnostics/patterns/qi-deficiency.md) · [혈허](diagnostics/patterns/blood-deficiency.md) · [담음](diagnostics/patterns/phlegm-fluid.md) · [어혈](diagnostics/patterns/blood-stasis.md) · [간울](diagnostics/patterns/liver-qi-stagnation.md) · [신허](diagnostics/patterns/kidney-deficiency.md)
<!-- PATTERN_AI_INDEX_15_END -->
'@
 Upsert "docs\ai-index.md" "<!-- PATTERN_AI_INDEX_15_START -->" "<!-- PATTERN_AI_INDEX_15_END -->" $ai

 Write-Host "PATTERN SYNDROME NETWORK EXPANSION 15 COMPLETE" -ForegroundColor Green
 Write-Host "8 pattern pages integrated into diagnostics, foundations, clinical-core, network and ai-index." -ForegroundColor Green
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
