$ErrorActionPreference="Stop"
function UpsertBlock($file,$start,$end,$block){
 if(-not(Test-Path $file)){return}
 $t=Get-Content $file -Raw -Encoding UTF8
 if($t.Contains($start)){
   $pat=[regex]::Escape($start)+".*?"+[regex]::Escape($end)
   $t=[regex]::Replace($t,$pat,$block,[Text.RegularExpressions.RegexOptions]::Singleline)
 } else {$t=$t.TrimEnd()+"`r`n`r`n"+$block+"`r`n"}
 Set-Content $file $t -Encoding UTF8
}
try{
 $R=Split-Path -Parent $MyInvocation.MyCommand.Path; Set-Location $R
 if(-not(Test-Path "docs")){throw "docs folder not found. ZIP을 저장소 최상위에 풀어주세요."}
 $stamp=Get-Date -Format "yyyyMMdd-HHmmss"; $bk="_backup_tonic_deepening_"+$stamp
 New-Item -ItemType Directory -Force $bk|Out-Null

 foreach($p in @("docs\\herbs\\cervi-parvum-cornu.md","docs\\pillar\\tonic-recovery.md","docs\\network\\tonic-formula-compare.md","docs\\formulas\\index.md","docs\\ai-index.md")){
   if(Test-Path $p){Copy-Item $p (Join-Path $bk ([IO.Path]::GetFileName($p))) -Force}
 }

 New-Item -ItemType Directory -Force "docs\\clinical-guides"|Out-Null
 Copy-Item "_tonic_deepening_payload\\*.md" "docs\\clinical-guides\\" -Force

 $deer=@'
<!-- DEER_TONIC_CONNECT_START -->

## 녹용보약으로 검색했다면

녹용은 단독 약재 정보뿐 아니라 **보약 처방 안에서 어떤 역할을 하는지, 어떤 품질 기준으로 선택되는지, 어떤 보익 처방과 연결되는지** 함께 보면 이해가 더 쉽습니다.

- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)
- [보약 처방의 용량·출전·품질](../clinical-guides/tonic-formula-dose-source-quality.md)
- [보익·보약 처방 현대 연구 심화 지도](../clinical-guides/tonic-research-deep-guide.md)
- [보익·회복 허브](../pillar/tonic-recovery.md)
- [보익 처방 비교](../network/tonic-formula-compare.md)

<!-- DEER_TONIC_CONNECT_END -->
'@
 UpsertBlock "docs\\herbs\\cervi-parvum-cornu.md" "<!-- DEER_TONIC_CONNECT_START -->" "<!-- DEER_TONIC_CONNECT_END -->" $deer

 $tonic=@'
<!-- TONIC_DEEP_CONNECT_START -->

## 녹용보약·보익 처방 심화

보약을 단순히 '기운을 올리는 처방'으로만 보지 않고 **약재 품질, 원전과 처방 구조, 구성비, 탕전량, 실제 복용 설계, 현대 연구**까지 함께 살펴볼 수 있습니다.

- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)
- [보약 처방의 용량·출전·품질](../clinical-guides/tonic-formula-dose-source-quality.md)
- [보익·보약 처방 현대 연구 심화 지도](../clinical-guides/tonic-research-deep-guide.md)
- [녹용 약재 상세](../herbs/cervi-parvum-cornu.md)
- [보기·기혈쌍보 처방 계보](../network/tonic-formula-lineage.md)

<!-- TONIC_DEEP_CONNECT_END -->
'@
 UpsertBlock "docs\\pillar\\tonic-recovery.md" "<!-- TONIC_DEEP_CONNECT_START -->" "<!-- TONIC_DEEP_CONNECT_END -->" $tonic

 $compare=@'
<!-- TONIC_QUALITY_CONNECT_START -->

## 처방명만 비교하지 말고 품질·용량·출전까지 보기

같은 보익 처방도 **원전의 구조, 약재 비율, 제형, 탕전량, 원료 품질, 환자별 가감**에 따라 실제 처방의 성격이 달라질 수 있습니다.

- [보약 처방의 용량·출전·품질 심화](../clinical-guides/tonic-formula-dose-source-quality.md)
- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)
- [보익·보약 처방 현대 연구 심화](../clinical-guides/tonic-research-deep-guide.md)

<!-- TONIC_QUALITY_CONNECT_END -->
'@
 UpsertBlock "docs\\network\\tonic-formula-compare.md" "<!-- TONIC_QUALITY_CONNECT_START -->" "<!-- TONIC_QUALITY_CONNECT_END -->" $compare

 $fidx=@'
<!-- TONIC_FORMULA_DEEP_LINK_START -->

## 보익 처방을 더 깊게 비교하기

- [보약 처방의 용량·출전·품질](../clinical-guides/tonic-formula-dose-source-quality.md)
- [보익·보약 처방 현대 연구 심화 지도](../clinical-guides/tonic-research-deep-guide.md)
- [녹용보약 통합 가이드](../clinical-guides/deer-antler-tonic-guide.md)

<!-- TONIC_FORMULA_DEEP_LINK_END -->
'@
 UpsertBlock "docs\\formulas\\index.md" "<!-- TONIC_FORMULA_DEEP_LINK_START -->" "<!-- TONIC_FORMULA_DEEP_LINK_END -->" $fidx

 $aidx=@'
<!-- DEER_TONIC_AI_INDEX_START -->

## 녹용보약·보약 처방 심화

- [녹용보약 — 녹용 정보와 보익 처방 통합 가이드](clinical-guides/deer-antler-tonic-guide.md)
- [보약 처방의 용량·출전·품질](clinical-guides/tonic-formula-dose-source-quality.md)
- [보익·보약 처방 현대 연구 심화 지도](clinical-guides/tonic-research-deep-guide.md)
- [녹용 약재 상세](herbs/cervi-parvum-cornu.md)

<!-- DEER_TONIC_AI_INDEX_END -->
'@
 UpsertBlock "docs\\ai-index.md" "<!-- DEER_TONIC_AI_INDEX_START -->" "<!-- DEER_TONIC_AI_INDEX_END -->" $aidx

 Write-Host "DEER ANTLER + TONIC DEEPENING COMPLETE" -ForegroundColor Green
 Write-Host "Created 3 deep guide pages and connected deer-antler/tonic hubs." -ForegroundColor Green
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
