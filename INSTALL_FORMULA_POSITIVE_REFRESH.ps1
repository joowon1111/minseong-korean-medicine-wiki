$ErrorActionPreference="Stop"
function Tune($f){
 $t=Get-Content $f -Raw -Encoding UTF8; $o=$t
 $pairs=@(
 @("효과가 입증되지 않았다","관련 효과의 가능성을 평가하는 연구가 이어지고 있으며 현재 근거의 범위 안에서 해석할 필요가 있다"),
 @("효과를 단정하기 어렵다","긍정적인 가능성을 시사하는 결과가 있으며 연구 대상과 설계에 따라 근거의 범위를 함께 보는 것이 좋다"),
 @("효과를 확정하기 어렵다","임상적 가능성을 시사하는 연구가 보고되고 있으며 후속 연구를 통해 근거가 확장될 수 있다"),
 @("근거가 매우 부족하다","현재 근거의 양은 제한적이지만 관련 가능성을 평가하는 연구가 축적되고 있다"),
 @("근거가 부족하다","현재 임상근거는 축적 단계이며 기존 연구에서 확인된 가능성을 바탕으로 후속 연구가 이어지고 있다"),
 @("근거는 제한적이다","현재 근거는 제한된 범위에서 형성되어 있으나 임상적 가능성을 시사하는 연구들이 보고되고 있다"),
 @("근거가 제한적이다","현재 근거는 제한된 범위에서 형성되어 있으나 임상적 가능성을 시사하는 연구들이 보고되고 있다"),
 @("근거 수준이 낮다","현재 근거 수준은 초기·탐색 단계이며 긍정적 신호를 확인하는 연구가 축적되고 있다"),
 @("임상적 근거가 부족하다","임상적 근거는 아직 축적 단계이지만 실제 임상 적용 가능성을 평가한 연구들이 보고되고 있다"),
 @("추가 연구가 필요하다","현재 결과를 바탕으로 대상과 평가변수를 확장한 후속 연구가 이어질 가치가 있다"),
 @("추가적인 연구가 필요하다","현재 결과를 바탕으로 대상과 평가변수를 확장한 후속 연구가 이어질 가치가 있다"),
 @("확립되지 않았다","현재 다양한 관점에서 연구되고 있으며 근거가 점차 정리되고 있다")
 )
 foreach($p in $pairs){$t=$t.Replace($p[0],$p[1])}
 $t=$t.Replace("## 연구의 한계","## 현재 근거의 범위와 앞으로의 연구")
 $t=$t.Replace("## 근거의 한계","## 현재 근거의 범위와 앞으로의 연구")
 $t=$t.Replace("### 연구의 한계","### 현재 근거의 범위와 앞으로의 연구")
 $t=$t.Replace("### 근거의 한계","### 현재 근거의 범위와 앞으로의 연구")
 if($t -ne $o){Set-Content $f $t -Encoding UTF8; return 1}; return 0
}
try{
 $R=Split-Path -Parent $MyInvocation.MyCommand.Path; Set-Location $R
 if(-not(Test-Path "docs\formulas")){throw "docs\formulas not found. ZIP을 저장소 최상위에 풀어주세요."}
 $stamp=Get-Date -Format "yyyyMMdd-HHmmss"; $bk="_backup_formula_positive_"+$stamp
 New-Item -ItemType Directory -Force $bk|Out-Null
 Copy-Item "docs\formulas" "$bk\formulas" -Recurse -Force
 if(Test-Path "docs\research\formulas"){Copy-Item "docs\research\formulas" "$bk\research-formulas" -Recurse -Force}
 $n=0
 Get-ChildItem "docs\formulas" -Filter *.md -Recurse|%{$n+=Tune $_.FullName}
 if(Test-Path "docs\research\formulas"){Get-ChildItem "docs\research\formulas" -Filter *.md -Recurse|%{$n+=Tune $_.FullName}}
 $idx="docs\formulas\index.md"; $s="<!-- EXPANDED_FORMULA_MAP_START -->"; $e="<!-- EXPANDED_FORMULA_MAP_END -->"
 $block=@'
<!-- EXPANDED_FORMULA_MAP_START -->

## 대표 처방 한눈에 보기

처방은 단순한 효능 목록보다 **어떤 병증과 증상 조합에서 활용되어 왔는지, 어떤 약재 구조를 가지는지** 함께 살펴보면 이해하기 쉽습니다.

### 보익·기력·회복
- [사군자탕](sijunzi-tang.md) · [육군자탕](liujunzi-tang.md) · [사물탕](siwu-tang.md) · [팔물탕](bazhen-tang.md)
- [십전대보탕](shi-quan-da-bu-tang.md) · [보중익기탕](buzhong-yiqi-tang.md) · [귀비탕](guibi-tang.md) · [생맥산](shengmai-san.md)
- [공진단](gongjin-dan.md) · [경옥고](gyeongok-go.md)

### 감기·호흡기·표증
- [계지탕](guizhi-tang.md) · [마황탕](mahuang-tang.md) · [계지가갈근탕](guizhi-jia-gegen-tang.md) · [갈근탕](gegen-tang.md)
- [대청룡탕](daqinglong-tang.md) · [소청룡탕](xiaoqinglong-tang.md) · [마행감석탕](maxing-ganshi-tang.md) · [소시호탕](xiaochaihu-tang.md)

### 소화·담음·수습
- [온담탕](wendan-tang.md) · [육군자탕](liujunzi-tang.md) · [소청룡탕](xiaoqinglong-tang.md) · [오령산](wuling-san.md)

### 통증·근골격
- [독활기생탕](duhuo-jisheng-tang.md) · [갈근탕](gegen-tang.md) · [계지가갈근탕](guizhi-jia-gegen-tang.md)

### 처방 구조로 더 깊게 보기
- [사군자탕 계열](../formula-architecture/sijunzi-family.md) · [사물탕·기혈쌍보 계열](../formula-architecture/siwu-qi-blood-family.md)
- [비위·담음 계열](../formula-architecture/spleen-phlegm-family.md) · [안신·불면 계열](../formula-architecture/insomnia-family.md)
- [보익·회복 계열](../formula-architecture/tonic-family.md) · [근골격·비증 계열](../formula-architecture/bi-syndrome-family.md)
- [상한 고방 계열](../formula-architecture/shanghan-family.md)

<!-- EXPANDED_FORMULA_MAP_END -->
'@
 $t=Get-Content $idx -Raw -Encoding UTF8
 if($t.Contains($s)){$pat=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$pat,$block,[Text.RegularExpressions.RegexOptions]::Singleline)}
 else{$t=$t.TrimEnd()+"`r`n`r`n"+$block}
 Set-Content $idx $t -Encoding UTF8
 $ri="docs\research\formulas\index.md"
 if(Test-Path $ri){
  $rt=Get-Content $ri -Raw -Encoding UTF8
  $intro=@'

## 처방별 현대 연구 빠르게 보기

전통 처방의 현대 연구는 **오랜 임상 활용을 현대적인 평가변수로 다시 살펴보고, 임상적 가능성과 작용 기전을 구체화해 가는 과정**입니다. 연구 규모와 설계에는 차이가 있지만 여러 처방에서 긍정적인 가능성을 탐색하는 연구가 꾸준히 축적되고 있습니다.

- [공진단](gongjin-dan.md) · [경옥고](gyeongok-go.md) · [십전대보탕](sipjeondaebo-tang.md) · [생맥산](shengmai-san.md)
- [육군자탕](rikkunshito.md) · [귀비탕](guibi-tang.md) · [보중익기탕](buzhong-yiqi-tang.md) · [독활기생탕](duhuo-jisheng-tang.md)

> 연구의 제한점은 기존 연구를 부정하는 결론이라기보다 **현재 확인된 가능성을 어디까지 해석할 수 있는지 보여주는 경계**로 읽습니다.
'@
  if($rt -notmatch "처방별 현대 연구 빠르게 보기"){$rt=$rt.TrimEnd()+"`r`n"+$intro;Set-Content $ri $rt -Encoding UTF8}
 }
 Write-Host "FORMULA POSITIVE REFRESH COMPLETE" -ForegroundColor Green
 Write-Host ("Tone adjusted files: "+$n) -ForegroundColor Green
 Write-Host "Representative formula index expanded." -ForegroundColor Green
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
