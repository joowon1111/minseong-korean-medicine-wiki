$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "CORE_HUB_BACKUP_STEP2"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_CORE_HUB_CONTENT_V1 -->"

$Items=@(
@{File="conditions/index.md"; Desc="환자가 실제로 사용하는 증상·생활언어에서 질환, 위험신호, 한의학적 병증, 한약·침구 지식으로 연결하는 증상·질환 허브입니다."; Intro=@"
## 증상·질환을 어떻게 찾나요?

질환명을 정확히 몰라도 괜찮습니다. **피곤해요, 소화가 안 돼요, 잠이 안 와요, 허리가 아파요, 손발이 차요**처럼 실제 불편한 표현에서 시작할 수 있습니다.

### 많이 찾는 영역

- **피로·회복** — 만성피로, 기력저하, 수술 후 회복, 노인 허약
- **소화** — 더부룩함, 체기, 식욕저하, 복부불편
- **수면·자율신경** — 불면, 새벽각성, 두근거림, 긴장성 증상
- **근골격 통증** — 목, 어깨, 허리, 무릎, 근육뭉침, 저림
- **여성·소아·생애주기** — 임신준비, 산후, 갱년기, 성장기
- **비뇨기·순환·냉증** — 야간뇨, 잔뇨감, 부종, 손발냉증

각 문서는 **위험신호와 감별 → 증상패턴 → 한의학적 병증 → 한약·침·전침·약침 → 관련 전문지식** 순으로 더 깊게 탐색할 수 있도록 연결합니다.
"@},
@{File="herbs/index.md"; Desc="한약에 사용되는 주요 본초를 효능·성미·귀경·병증·방제 속 역할과 함께 탐색하는 본초학 허브입니다."; Intro=@"
## 본초를 어떻게 찾나요?

본초는 특정 약재의 효능 한 줄로만 이해하기보다 **성미·귀경·효능·병증·배합관계와 실제 처방 속 역할**을 함께 보는 것이 중요합니다.

- 피로·기력회복 → 인삼, 황기, 백출, 당귀, 숙지황, 녹용
- 소화·비위 → 백출, 진피, 반하, 복령, 사인, 후박
- 통증·근골격 → 독활, 두충, 우슬, 속단, 천궁, 작약
- 수면·심계 → 산조인, 원지, 복신, 백자인
- 여성·월경 → 당귀, 천궁, 작약, 향부자

환자 검색어에서 본초로 들어온 뒤 다시 **병증 → 방제 → 임상 활용 → 근거**로 연결해 볼 수 있습니다.
"@},
@{File="formulas/index.md"; Desc="주요 한약 처방을 병증·치법·구성 본초·적용 증상·고전 출전과 함께 탐색하는 방제학 허브입니다."; Intro=@"
## 방제를 어떻게 찾나요?

같은 피로·소화불량·불면·통증이라도 한열·허실·기혈진액과 동반증상에 따라 처방은 달라질 수 있습니다.

- 피로·허약 → 보중익기탕, 팔물탕, 십전대보탕, 생맥산 등
- 소화 → 평위산, 향사육군자탕, 반하사심탕, 이진탕 등
- 불면·심계 → 귀비탕, 온담탕, 천왕보심단, 산조인탕 등
- 통증 → 독활기생탕, 오적산, 회수산 등

처방명은 출발점이며 실제 처방은 **현재 병증과 환자 상태를 평가하여 가감·선택**합니다.
"@},
@{File="tonic-masterpieces/deer-antler/index.md"; Desc="녹용의 한의학적 성미·귀경·전통적 활용, 부위와 품질, 보익 처방에서의 배합과 현대 연구를 연결한 녹용 심화 허브입니다."; Intro=@"
## 녹용을 한의학적으로 이해하기

녹용은 보익 본초 가운데 중요한 약재로, 단독 성분 하나의 효과만으로 보기보다 **환자의 기력·회복상태·소화·수면·냉열과 다른 본초와의 배합**을 함께 살펴 이해하는 것이 중요합니다.

이 허브에서는 녹용의 **부위·품질·전통적 본초학적 성격·처방 속 역할·임상 활용·현대 연구**를 단계적으로 연결합니다.

### 함께 살펴볼 주제

- 녹용의 부위와 품질, 분골
- 허약·기력저하·회복기와 보익 개념
- 인삼·황기·숙지황·당귀 등 보익 본초와의 배합
- 녹용이 포함되는 처방 구조
- 현대 연구를 읽을 때 전통적 활용과 임상근거를 구분하는 방법
"@},
@{File="tonic-masterpieces/deer-antler/clinical-map.md"; Desc="녹용을 기력저하·허약·회복기·연령별 보약 수요에서 병증, 본초 배합, 맞춤한약과 연결하는 임상 활용 지도입니다."; Intro=@"
## 녹용 임상 활용을 보는 순서

녹용을 찾는 이유는 다양합니다. **기력이 떨어졌어요, 부모님 보약, 수험생 체력, 수술 후 회복, 만성피로**처럼 환자의 목적에서 시작해 현재 상태를 구체적으로 나누는 것이 중요합니다.

1. 피로와 허약의 원인·기간·회복속도를 확인합니다.
2. 식욕·소화·수면·냉열·근력과 연령을 함께 봅니다.
3. 기허·혈허·기혈양허·신허 등 병증을 구분합니다.
4. 녹용을 다른 보익 본초와 어떻게 배합할지 살펴봅니다.
5. 일정 기간 후 피로·식사·수면·활동 후 회복 같은 지표를 재평가합니다.

녹용은 모든 피로에 동일하게 적용하는 개념이 아니라 **맞춤 처방 안에서 역할을 갖는 본초**로 이해합니다.
"@},
@{File="tonic-masterpieces/deer-antler/quality-parts.md"; Desc="녹용의 분골 등 부위 구분과 품질을 본초학적·임상적 관점에서 이해하기 위한 안내입니다."; Intro=@"
## 녹용의 부위와 품질을 왜 구분하나요?

녹용은 한 덩어리의 동일한 원료로만 보지 않고 **채취 부위와 조직 특성, 가공·규격과 품질관리**를 함께 살펴볼 필요가 있습니다. 특히 분골 등 부위 명칭은 실제 한약 상담에서 자주 접하는 표현입니다.

품질을 평가할 때는 단순히 특정 부위가 무조건 우수하다고 단정하기보다 **원산지·규격·가공·보관·처방 목적과 배합**을 함께 보는 것이 적절합니다.
"@},
@{File="tonic-masterpieces/gongjindan/index.md"; Desc="공진단의 처방 구성과 전통적 활용, 피로·기력·회복 관점의 임상 활용과 현대 연구를 연결한 심화 허브입니다."; Intro=@"
## 공진단을 어떻게 이해하나요?

공진단은 이름 자체보다 **처방 구성, 전통적 적응 개념, 현재 환자의 피로·수면·소화·회복상태**를 함께 보는 것이 중요합니다.

아카이브에서는 공진단을 단순 건강제품으로 다루지 않고 **방제 구조 → 구성 본초 → 병증 → 임상 활용 → 현대 연구**의 순서로 살펴봅니다.
"@},
@{File="tonic-masterpieces/gyeongokgo/index.md"; Desc="경옥고의 처방 구성과 전통적 보익 개념, 피로·허약·진액 상태와 현대 연구를 연결한 심화 허브입니다."; Intro=@"
## 경옥고를 어떻게 이해하나요?

경옥고는 보익 처방의 하나로서 **피로·허약·소화·건조감·연령과 현재 병증**을 함께 살펴 이해합니다.

공진단·녹용보약과 단순 우열을 비교하기보다 각 처방의 구성과 목표, 환자의 현재 상태가 어떻게 다른지를 보는 것이 중요합니다.
"@}
)

function Add-Description([string]$text,[string]$desc){
    if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
        $fm=$Matches[1]
        if($fm -match '(?m)^description:\s*.*$'){
            $newfm=[regex]::Replace($fm,'(?m)^description:\s*.*$',"description: $desc",1)
        } else { $newfm=$fm.TrimEnd()+"`r`ndescription: $desc" }
        return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$newfm`r`n---",1)
    } else {
        return "---`r`ndescription: $desc`r`n---`r`n"+$text
    }
}

$changed=0
foreach($item in $Items){
    $p=Join-Path $Docs $item.File
    if(-not (Test-Path $p)){ Write-Host "SKIP missing: $($item.File)" -ForegroundColor Yellow; continue }
    $text=Get-Content $p -Raw -Encoding UTF8
    if($text.Contains($Marker)){ Write-Host "SKIP already enriched: $($item.File)"; continue }

    $backup=Join-Path $Backup $item.File
    New-Item -ItemType Directory -Force -Path (Split-Path $backup -Parent) | Out-Null
    Copy-Item $p $backup -Force

    $text=Add-Description $text $item.Desc
    $addition="`r`n`r`n$Marker`r`n"+$item.Intro.Trim()+"`r`n"
    Set-Content $p ($text.TrimEnd()+$addition) -Encoding UTF8
    Write-Host "ENRICHED: $($item.File)" -ForegroundColor Green
    $changed++
}
Write-Host ""
Write-Host "STEP 2 완료: $changed 개 핵심 허브 본문·description 보강" -ForegroundColor Cyan
Write-Host "원본 백업: CORE_HUB_BACKUP_STEP2"
Read-Host "Enter를 누르면 종료합니다"
