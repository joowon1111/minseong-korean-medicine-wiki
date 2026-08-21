$ErrorActionPreference="Stop"
function Upsert($f,$s,$e,$b){if(-not(Test-Path $f)){return};$t=Get-Content $f -Raw -Encoding UTF8;if($t.Contains($s)){$p=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b+"`r`n"};Set-Content $f $t -Encoding UTF8}
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs\\herbs")){throw "docs\\herbs not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_gyeongokgo_final_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\\formulas\\gyeongok-go.md","docs\\network\\gyeongok-composition.md","docs\\network\\gyeongok-go-map.md","docs\\herbs\\index.md","docs\\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ([IO.Path]::GetFileName($p))) -Force}}
Copy-Item "_gyeongokgo_payload\\rehmannia-root-fresh.md" "docs\\herbs\\" -Force
Copy-Item "_gyeongokgo_payload\\honey.md" "docs\\herbs\\" -Force
New-Item -ItemType Directory -Force "docs\\clinical-guides"|Out-Null
Copy-Item "_gyeongokgo_payload\\gyeongokgo-composition-quality-guide.md" "docs\\clinical-guides\\" -Force
$g=@'
<!-- GYEONGOK_CORE_HERBS_START -->
## 경옥고의 네 핵심 구성
경옥고는 **인삼·생지황·복령·봉밀**이 서로 다른 역할을 맡는 전통 고제입니다.

| 구성 | 처방 안에서 보는 핵심 |
|---|---|
| [인삼](../herbs/ginseng.md) | 보기·원기 |
| [생지황](../herbs/rehmannia-root-fresh.md) | 양음·생진 |
| [복령](../herbs/poria.md) | 건비·수습 |
| [봉밀](../herbs/honey.md) | 윤조·완급·조화와 고제의 바탕 |

[경옥고 구성·원료·제조 품질 가이드 →](../clinical-guides/gyeongokgo-composition-quality-guide.md)
<!-- GYEONGOK_CORE_HERBS_END -->
'@
Upsert "docs\\formulas\\gyeongok-go.md" "<!-- GYEONGOK_CORE_HERBS_START -->" "<!-- GYEONGOK_CORE_HERBS_END -->" $g
$n=@'
<!-- GYEONGOK_COMPOSITION_DEEP_START -->
## 네 본초로 읽는 경옥고
- [인삼](../herbs/ginseng.md) — 보기
- [생지황](../herbs/rehmannia-root-fresh.md) — 양음·생진
- [복령](../herbs/poria.md) — 건비·수습
- [봉밀](../herbs/honey.md) — 윤조·조화·고제 제형

**보기 + 자음생진 + 건비 + 윤조·조화**라는 네 축으로 경옥고의 구조를 볼 수 있습니다.

[경옥고 원료·제조 품질 심화 →](../clinical-guides/gyeongokgo-composition-quality-guide.md)
<!-- GYEONGOK_COMPOSITION_DEEP_END -->
'@
Upsert "docs\\network\\gyeongok-composition.md" "<!-- GYEONGOK_COMPOSITION_DEEP_START -->" "<!-- GYEONGOK_COMPOSITION_DEEP_END -->" $n
Upsert "docs\\network\\gyeongok-go-map.md" "<!-- GYEONGOK_COMPOSITION_DEEP_START -->" "<!-- GYEONGOK_COMPOSITION_DEEP_END -->" $n
$h=@'
<!-- GYEONGOK_HERBS_INDEX_START -->
### 경옥고 구성 본초
[인삼](ginseng.md) · [생지황](rehmannia-root-fresh.md) · [복령](poria.md) · [봉밀](honey.md)

→ [경옥고 구성·원료·제조 품질 가이드](../clinical-guides/gyeongokgo-composition-quality-guide.md)
<!-- GYEONGOK_HERBS_INDEX_END -->
'@
Upsert "docs\\herbs\\index.md" "<!-- GYEONGOK_HERBS_INDEX_START -->" "<!-- GYEONGOK_HERBS_INDEX_END -->" $h
$a=@'
<!-- GYEONGOK_AI_START -->
### 경옥고 핵심 구성
[경옥고](formulas/gyeongok-go.md) → [인삼](herbs/ginseng.md) · [생지황](herbs/rehmannia-root-fresh.md) · [복령](herbs/poria.md) · [봉밀](herbs/honey.md) → [원료·제조 품질 심화](clinical-guides/gyeongokgo-composition-quality-guide.md)
<!-- GYEONGOK_AI_END -->
'@
Upsert "docs\\ai-index.md" "<!-- GYEONGOK_AI_START -->" "<!-- GYEONGOK_AI_END -->" $a
Write-Host "GYEONGOKGO FINAL EXPANSION COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"
