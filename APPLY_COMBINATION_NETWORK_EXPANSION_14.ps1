$ErrorActionPreference="Stop"
function Upsert($f,$s,$e,$b){if(-not(Test-Path $f)){return};$t=Get-Content $f -Raw -Encoding UTF8;if($t.Contains($s)){$p=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b};Set-Content $f $t -Encoding UTF8}
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs\clinical-core\index.md")){throw "clinical-core hub not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_combination14_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\clinical-core\index.md","docs\herbs\index.md","docs\formulas\index.md","docs\acupuncture\index.md","docs\pillar\acupuncture-treatment.md","docs\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\","_"))) -Force}}
New-Item -ItemType Directory -Force "docs\network"|Out-Null
$ac=@'
---
title: 임상 핵심 배혈 조합 지도
description: 임상에서 자주 함께 고려하는 경혈 조합을 증상과 치료 목표에 따라 연결합니다.
tags: [경혈, 배혈, 침구, 임상한의학]
---
# 임상 핵심 배혈 조합 지도

경혈은 한 혈의 주치만 보기보다 **국소혈 + 원위혈, 경락 관계, 병증과 치료 목표**를 함께 보면서 배혈합니다.

## 소화불량·더부룩함
**족삼리 ST36 + 중완 CV12 + 내관 PC6**
- [족삼리](../acupuncture/points/st36-zusanli.md)
- [중완](../acupuncture/points/cv12-zhongwan.md)
- [내관](../acupuncture/points/pc6-neiguan.md)
→ [소화불량 임상 연결](../clinical-core/pathways/dyspepsia.md)

## 불면·긴장·두근거림
**신문 HT7 + 내관 PC6 + 인당 EX-HN3**
- [신문](../acupuncture/points/ht7-shenmen.md)
- [내관](../acupuncture/points/pc6-neiguan.md)
- [인당](../acupuncture/points/ex-hn3-yintang.md)
→ [불면 임상 연결](../clinical-core/pathways/insomnia.md)

## 요통
**대장수 BL25 + 위중 BL40 + 곤륜 BL60**
→ [요통 임상 연결](../clinical-core/pathways/low-back-pain.md)

## 여성 냉증·생리증상
**삼음교 SP6 + 관원 CV4 + 태충 LR3**
→ [여성 임상 연결](../clinical-core/pathways/women-cold-blood.md)

## 무릎·하지
**양릉천 GB34 + 족삼리 ST36 + 음릉천 SP9**
→ [무릎·하지통증 임상 연결](../clinical-core/pathways/knee-leg-pain.md)

## 호흡기·비염
**열결 LU7 + 합곡 LI4 + 인당 EX-HN3**
→ [비염·기침 임상 연결](../clinical-core/pathways/rhinitis-cough.md)

## 배혈을 읽는 원칙
배혈은 고정 공식이 아니라 **주증 + 동반증상 + 경락 + 국소조직 + 전신 병증**을 조합하는 과정입니다.

## 현대 연구
침 임상연구에서는 복합 배혈 프로토콜이 널리 사용됩니다. 혈위 조합, 자침·전침 방법, 치료 횟수와 평가변수를 함께 확인합니다.
'@
Set-Content "docs\network\acupoint-combinations.md" $ac -Encoding UTF8
$hp=@'
---
title: 임상 핵심 본초 배합 지도 — 약대
description: 임상 처방에서 자주 함께 이해하는 본초 쌍을 병증과 대표 방제에 따라 연결합니다.
tags: [본초, 약대, 배합, 방제]
---
# 임상 핵심 본초 배합 지도 — 약대

## 반하 + 진피
**화담 + 이기**의 대표 조합입니다.
[반하](../herbs/pinellia.md) · [진피](../herbs/citrus-peel.md) → [이진탕](../formulas/erchen-tang.md) · [육군자탕](../formulas/liujunzi-tang.md)

## 인삼 + 황기
보기의 두 축을 비교합니다.
[인삼](../herbs/ginseng.md) · [황기](../herbs/astragalus-tonic-guide.md) → [보중익기탕](../formulas/buzhong-yiqi-tang.md)

## 당귀 + 백작약
보혈·양혈의 조화를 봅니다.
[당귀](../herbs/angelica.md) · [백작약](../herbs/white-peony.md) → [사물탕](../formulas/siwu-tang.md)

## 두충 + 우슬
간신·근골과 하체를 함께 봅니다.
[두충](../herbs/eucommia.md) · [우슬](../herbs/achyranthes.md) → [독활기생탕](../formulas/duhuo-jisheng-tang.md)

## 산조인 + 원지
안신을 중심으로 수면·심계·건망을 연결합니다.
[산조인](../herbs/jujube-seed.md) · [원지](../herbs/polygala.md) → [귀비탕](../formulas/guibi-tang.md) · [천왕보심단](../formulas/tianwang-buxin-dan.md)

## 맥문동 + 오미자
양음생진과 수렴을 함께 봅니다.
[맥문동](../herbs/ophiopogon.md) · [오미자](../herbs/schisandra.md) → [생맥산](../formulas/shengmai-san.md)

## 도인 + 홍화
활혈거어를 이해하는 대표 조합입니다.
[도인](../herbs/peach-kernel.md) · [홍화](../herbs/safflower.md)

## 배합을 읽는 원칙
약대는 고정 공식이 아니라 전체 방제의 **군신좌사·한열허실·구성비** 안에서 해석합니다.
'@
Set-Content "docs\network\herb-pair-combinations.md" $hp -Encoding UTF8
$fp=@'
---
title: 방제·경혈 임상 조합 지도
description: 같은 병증을 한약 처방과 침구 배혈에서 어떻게 연결해 보는지 정리합니다.
tags: [방제, 경혈, 침구, 임상한의학]
---
# 방제·경혈 임상 조합 지도

## 비위허약·소화불량
**육군자탕·향사육군자탕 ↔ 족삼리·중완·내관**
→ [소화불량 임상 경로](../clinical-core/pathways/dyspepsia.md)

## 수면·심계
**귀비탕·산조인탕 ↔ 신문·내관·인당**
→ [불면 임상 경로](../clinical-core/pathways/insomnia.md)

## 한습·어혈성 근골격 통증
**오적산·소경활혈탕 ↔ 대장수·위중·곤륜**
→ [요통 임상 경로](../clinical-core/pathways/low-back-pain.md)

## 여성 냉증·어혈
**온경탕·계지복령환 ↔ 삼음교·관원·태충**
→ [여성 임상 경로](../clinical-core/pathways/women-cold-blood.md)

## 기허·회복저하
**보중익기탕·십전대보탕 ↔ 족삼리·기해·관원**
→ [피로·회복 임상 경로](../clinical-core/pathways/fatigue-recovery.md)

## 해석 원칙
한약과 침구를 같은 효능으로 단순 대응시키지 않고 **병증·치법이라는 공통 언어**를 중심으로 연결합니다.
'@
Set-Content "docs\network\formula-acupoint-combinations.md" $fp -Encoding UTF8
$b=@'
<!-- COMBINATION_NETWORK_14_START -->
## 임상 조합 네트워크
- [임상 핵심 배혈 조합 지도](../network/acupoint-combinations.md)
- [임상 핵심 본초 배합 지도 — 약대](../network/herb-pair-combinations.md)
- [방제·경혈 임상 조합 지도](../network/formula-acupoint-combinations.md)
<!-- COMBINATION_NETWORK_14_END -->
'@
Upsert "docs\clinical-core\index.md" "<!-- COMBINATION_NETWORK_14_START -->" "<!-- COMBINATION_NETWORK_14_END -->" $b
$h=@'
<!-- COMBO_HERB_14_START -->
## 본초 배합으로 더 깊게 보기
- [임상 핵심 본초 배합 지도 — 약대](../network/herb-pair-combinations.md)
<!-- COMBO_HERB_14_END -->
'@
Upsert "docs\herbs\index.md" "<!-- COMBO_HERB_14_START -->" "<!-- COMBO_HERB_14_END -->" $h
$f=@'
<!-- COMBO_FORMULA_14_START -->
## 방제와 경혈을 함께 보기
- [방제·경혈 임상 조합 지도](../network/formula-acupoint-combinations.md)
<!-- COMBO_FORMULA_14_END -->
'@
Upsert "docs\formulas\index.md" "<!-- COMBO_FORMULA_14_START -->" "<!-- COMBO_FORMULA_14_END -->" $f
$a=@'
<!-- COMBO_ACU_14_START -->
## 배혈 조합으로 더 깊게 보기
- [임상 핵심 배혈 조합 지도](../network/acupoint-combinations.md)
<!-- COMBO_ACU_14_END -->
'@
Upsert "docs\acupuncture\index.md" "<!-- COMBO_ACU_14_START -->" "<!-- COMBO_ACU_14_END -->" $a
Upsert "docs\pillar\acupuncture-treatment.md" "<!-- COMBO_ACU_14_START -->" "<!-- COMBO_ACU_14_END -->" $a
Write-Host "COMBINATION NETWORK EXPANSION 14 COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"
