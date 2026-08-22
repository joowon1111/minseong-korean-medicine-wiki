$ErrorActionPreference="Stop"
function U($f,$s,$e,$b){if(!(Test-Path $f)){return};$t=Get-Content $f -Raw -Encoding UTF8;if($t.Contains($s)){$p=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b};Set-Content $f $t -Encoding UTF8}
try{$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(!(Test-Path "docs")){throw "docs folder not found"}
$bk="_backup_three_hubs18_"+(Get-Date -Format "yyyyMMdd-HHmmss");New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\herbs\index.md","docs\formulas\index.md","docs\clinical-core\index.md","docs\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\","_"))) -Force}}
$h=@'
<!-- THREE_CORE_HERB_HUB_18_START -->
## 임상 본초 지식망
본초는 **병증 → 본초군 → 약대 → 대표 방제 → 임상 증상**으로 연결해 봅니다.

### 영역별 핵심 본초
- **보기·회복**: 인삼 · 황기 · 백출 · 복령 · 녹용
- **보혈·기혈**: 당귀 · 백작약 · 숙지황 · 천궁
- **소화·담음**: 반하 · 진피 · 후박 · 사인 · 복령
- **안신·수면**: 산조인 · 원지 · 맥문동 · 오미자
- **활혈·어혈**: 단삼 · 도인 · 홍화 · 당귀
- **근골·풍습**: 두충 · 우슬 · 독활 · 강활 · 의이인
- **간울**: 시호 · 백작약 · 진피
- **신허·보익**: 숙지황 · 산수유 · 두충 · 녹용

### 배합·변증·증상으로 더 깊게
- [임상 핵심 본초 배합 지도 — 약대](../network/herb-pair-combinations.md)
- [임상 핵심 변증 지도](../diagnostics/patterns/index.md)
- [임상 변증 감별 지도](../diagnostics/differentials/index.md)
- [임상 핵심 본초·방제·경혈](../clinical-core/index.md)
<!-- THREE_CORE_HERB_HUB_18_END -->
'@
U "docs\herbs\index.md" "<!-- THREE_CORE_HERB_HUB_18_START -->" "<!-- THREE_CORE_HERB_HUB_18_END -->" $h
$f=@'
<!-- THREE_CORE_FORMULA_HUB_18_START -->
## 임상 방제 지식망
방제는 **병증·치법 → 처방 구조 → 구성 본초 → 환자 증상 → 침구치료**로 연결합니다.

### 영역별 대표 방제
- **보기·회복**: 사군자탕 · 육군자탕 · 팔물탕 · 십전대보탕 · 보중익기탕 · 귀비탕
- **소화·담음**: 평위산 · 이진탕 · 반하사심탕 · 향사육군자탕 · 삼령백출산 · 보화환 · 온담탕
- **수면·심계**: 귀비탕 · 산조인탕 · 천왕보심단 · 시호가용골모려탕
- **통증·풍습·어혈**: 독활기생탕 · 오적산 · 소경활혈탕 · 당귀수산 · 작약감초탕
- **여성**: 온경탕 · 당귀작약산 · 계지복령환 · 가미소요산
- **호흡기**: 소청룡탕 · 맥문동탕 · 삼소음
- **신허**: 육미지황환 · 팔미지황환
- **대표 보익**: 공진단 · 경옥고

### 변증·경혈·연구로 더 깊게
- [임상 핵심 변증 지도](../diagnostics/patterns/index.md)
- [방제·경혈 임상 조합 지도](../network/formula-acupoint-combinations.md)
- [처방 구조 비교](../formula-architecture/index.md)
- [현대 임상근거](../pillar/clinical-evidence.md)
<!-- THREE_CORE_FORMULA_HUB_18_END -->
'@
U "docs\formulas\index.md" "<!-- THREE_CORE_FORMULA_HUB_18_START -->" "<!-- THREE_CORE_FORMULA_HUB_18_END -->" $f
$c=@'
<!-- THREE_CORE_BALANCE_18_START -->
## 본초·방제·경혈 3대 임상 허브
| 시작점 | 연결 |
|---|---|
| **본초** | [본초학 임상 지식망](../herbs/index.md) |
| **방제** | [방제학 임상 지식망](../formulas/index.md) |
| **경혈** | [경혈 임상 지식망](../acupoint-network/) |

세 축은 **환자 질문 → 증상 → 변증 → 본초·방제·경혈 → 치료 → 연구** 흐름으로 서로 연결됩니다.
<!-- THREE_CORE_BALANCE_18_END -->
'@
U "docs\clinical-core\index.md" "<!-- THREE_CORE_BALANCE_18_START -->" "<!-- THREE_CORE_BALANCE_18_END -->" $c
$a=@'
<!-- THREE_CORE_AI_18_START -->
## 임상 핵심 3대 지식망
- [본초학 임상 지식망](herbs/index.md)
- [방제학 임상 지식망](formulas/index.md)
- [경혈 임상 지식망](acupoint-network/)
- [본초·방제·경혈 통합 허브](clinical-core/index.md)
<!-- THREE_CORE_AI_18_END -->
'@
U "docs\ai-index.md" "<!-- THREE_CORE_AI_18_START -->" "<!-- THREE_CORE_AI_18_END -->" $a
Write-Host "THREE CORE HUBS BALANCE 18 COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"