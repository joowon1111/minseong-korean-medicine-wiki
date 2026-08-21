$ErrorActionPreference="Stop"
function Upsert($f,$s,$e,$b){if(-not(Test-Path $f)){return};$t=Get-Content $f -Raw -Encoding UTF8;if($t.Contains($s)){$p=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b+"`r`n"};Set-Content $f $t -Encoding UTF8}
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs\\herbs")){throw "docs\\herbs not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_gongjin_herbs_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\\herbs","docs\\formulas\\gongjin-dan.md","docs\\network\\gongjin-composition.md","docs\\herbs\\index.md","docs\\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ([IO.Path]::GetFileName($p))) -Recurse -Force}}
Copy-Item "_gongjin_herbs_payload\\*.md" "docs\\herbs\\" -Force
$g=@'
<!-- GONGJIN_HERBS_EXPANDED_START -->
## 공진단 핵심 구성 본초
공진단은 약재 하나의 효능보다 **녹용·당귀·산수유·사향이 서로 어떤 역할을 맡는지** 구조로 보면 이해하기 쉽습니다.

| 본초 | 처방 안에서 보는 핵심 |
|---|---|
| [녹용](../herbs/cervi-parvum-cornu.md) | 보익·정혈·허약 회복의 축 |
| [당귀](../herbs/angelica.md) | 보혈과 혈행의 축 |
| [산수유](../herbs/cornus-fructus.md) | 간신 보익·수렴의 축 |
| [사향](../herbs/moschus.md) | 방향·개규·활혈의 축 |

[공진단 구성 본초 네트워크 →](../network/gongjin-composition.md)
<!-- GONGJIN_HERBS_EXPANDED_END -->
'@
Upsert "docs\\formulas\\gongjin-dan.md" "<!-- GONGJIN_HERBS_EXPANDED_START -->" "<!-- GONGJIN_HERBS_EXPANDED_END -->" $g
$n=@'
<!-- GONGJIN_COMPOSITION_DEEP_START -->
## 네 본초로 읽는 공진단
- [녹용](../herbs/cervi-parvum-cornu.md) — 보익
- [당귀](../herbs/angelica.md) — 보혈
- [산수유](../herbs/cornus-fructus.md) — 보익·수렴
- [사향](../herbs/moschus.md) — 방향·개규·활혈

**보익 → 보혈 → 수렴 → 움직임**이라는 네 축으로 보면 공진단의 처방 구조를 입체적으로 이해할 수 있습니다.
<!-- GONGJIN_COMPOSITION_DEEP_END -->
'@
Upsert "docs\\network\\gongjin-composition.md" "<!-- GONGJIN_COMPOSITION_DEEP_START -->" "<!-- GONGJIN_COMPOSITION_DEEP_END -->" $n
$h=@'
<!-- TONIC_HERBS_EXPANDED_START -->
## 보약을 이해할 때 함께 보면 좋은 핵심 본초
- [녹용](cervi-parvum-cornu.md) · [인삼](ginseng.md) · [황기](astragalus-tonic-guide.md) · [당귀](angelica.md)
- [숙지황](rehmannia-preparata.md) · [산수유](cornus-fructus.md) · [사향](moschus.md)
- [백출](atractylodes.md) · [복령](poria.md) · [감초](licorice.md)

보약의 완성도는 고가 약재 하나보다 **보기·보혈·자음·건비·수렴·활혈 등 각 본초가 전체 처방에서 어떤 균형을 이루는지** 함께 보는 것이 중요합니다.
<!-- TONIC_HERBS_EXPANDED_END -->
'@
Upsert "docs\\herbs\\index.md" "<!-- TONIC_HERBS_EXPANDED_START -->" "<!-- TONIC_HERBS_EXPANDED_END -->" $h
$a=@'
<!-- GONGJIN_HERBS_AI_START -->
### 공진단·보약 핵심 본초
[녹용](herbs/cervi-parvum-cornu.md) · [당귀](herbs/angelica.md) · [산수유](herbs/cornus-fructus.md) · [사향](herbs/moschus.md) · [숙지황](herbs/rehmannia-preparata.md) · [황기](herbs/astragalus-tonic-guide.md)
<!-- GONGJIN_HERBS_AI_END -->
'@
Upsert "docs\\ai-index.md" "<!-- GONGJIN_HERBS_AI_START -->" "<!-- GONGJIN_HERBS_AI_END -->" $a
Write-Host "GONGJIN + TONIC HERBS EXPANSION COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"
