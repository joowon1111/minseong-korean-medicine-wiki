$ErrorActionPreference="Stop"
function Upsert($f,$s,$e,$b){if(-not(Test-Path $f)){return};$t=Get-Content $f -Raw -Encoding UTF8;if($t.Contains($s)){$p=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$p,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b+"`r`n"};Set-Content $f $t -Encoding UTF8}
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_tonic_atlas_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\clinical-guides","docs\formulas\index.md","docs\pillar\tonic-recovery.md","docs\herbs\cervi-parvum-cornu.md","docs\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ([IO.Path]::GetFileName($p))) -Recurse -Force}}
New-Item -ItemType Directory -Force "docs\clinical-guides"|Out-Null;Copy-Item "_tonic_atlas_payload\tonic-formula-design-dose-atlas.md" "docs\clinical-guides\" -Force
$b=@'
<!-- TONIC_ATLAS_LINK_START -->
## 보익 처방 설계·용량 아틀라스
사군자탕·사물탕·팔물탕·십전대보탕·보중익기탕·귀비탕·육군자탕·생맥산을 **출전 → 원방 구조 → 상대 구성비 → 현대적 가감 → 녹용 가미** 순으로 비교합니다.

[보익 처방 설계·용량 아틀라스 보기 →](../clinical-guides/tonic-formula-design-dose-atlas.md)
<!-- TONIC_ATLAS_LINK_END -->
'@
Upsert "docs\formulas\index.md" "<!-- TONIC_ATLAS_LINK_START -->" "<!-- TONIC_ATLAS_LINK_END -->" $b;Upsert "docs\pillar\tonic-recovery.md" "<!-- TONIC_ATLAS_LINK_START -->" "<!-- TONIC_ATLAS_LINK_END -->" $b
$d=@'
<!-- DEER_ATLAS_LINK_START -->
## 녹용을 어떤 처방 구조에 연결할 것인가?
녹용의 양만 비교하기보다 **어떤 기본 보익 처방에 녹용을 더하는지, 그 가미가 원방의 방향을 어떻게 강화하는지** 함께 봅니다.

[보익 처방 설계·용량 아틀라스 보기 →](../clinical-guides/tonic-formula-design-dose-atlas.md)
<!-- DEER_ATLAS_LINK_END -->
'@
Upsert "docs\herbs\cervi-parvum-cornu.md" "<!-- DEER_ATLAS_LINK_START -->" "<!-- DEER_ATLAS_LINK_END -->" $d
$a=@'
<!-- TONIC_ATLAS_AI_START -->
### 보익 처방 설계·용량 아틀라스
[사군자탕부터 귀비탕·십전대보탕까지 원방 구조와 녹용 가미 비교](clinical-guides/tonic-formula-design-dose-atlas.md)
<!-- TONIC_ATLAS_AI_END -->
'@
Upsert "docs\ai-index.md" "<!-- TONIC_ATLAS_AI_START -->" "<!-- TONIC_ATLAS_AI_END -->" $a
Write-Host "TONIC FORMULA ATLAS INSTALLED" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"
