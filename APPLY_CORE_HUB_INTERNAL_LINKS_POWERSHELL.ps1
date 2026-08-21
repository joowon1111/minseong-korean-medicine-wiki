$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "HUB_LINK_BACKUP_STEP1"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_CORE_HUB_LINKS_V2 -->"

$Hubs=@(
    @{File="conditions/deer-antler-tonic-guide.md"; Links=@(
        @("맞춤한약","custom-herbal-medicine.md"),@("기력회복·허약","energy-recovery.md"),
        @("노인보약·어르신보약","elderly-tonic.md"),@("수험생 체력·기력회복","student-stamina.md"),
        @("보약·영양제 함께 선택","tonic-vs-health-supplement.md"),
        @("피로·기력저하 한약 처방 찾기","../herbal-integrated/formula-for-fatigue.md"),
        @("피로·기력회복 본초 찾기","../herbal-integrated/herbs-for-fatigue.md")
    )},
    @{File="conditions/custom-herbal-medicine.md"; Links=@(
        @("보약은 언제 먹나요","when-to-take-tonic.md"),@("녹용보약","deer-antler-tonic-guide.md"),
        @("건강검진 후 한약·보약 상담","herbal-medicine-after-checkup.md"),
        @("영양제·건강기능식품과 한약","supplements-herbal-medicine.md"),
        @("증상·치법으로 본초·방제 찾기","../herbal-integrated/by-symptom-treatment.md"),
        @("같은 증상인데 처방이 다른 이유","../herbal-integrated/formula-selection-guide.md")
    )},
    @{File="conditions/energy-recovery.md"; Links=@(
        @("만성피로","chronic-fatigue.md"),@("노인보약·어르신보약","elderly-tonic.md"),
        @("녹용보약","deer-antler-tonic-guide.md"),@("맞춤한약","custom-herbal-medicine.md"),
        @("피로·기력저하 한약 처방 찾기","../herbal-integrated/formula-for-fatigue.md")
    )},
    @{File="conditions/chronic-fatigue.md"; Links=@(
        @("기력회복·허약","energy-recovery.md"),@("맞춤한약","custom-herbal-medicine.md"),
        @("녹용보약","deer-antler-tonic-guide.md"),@("불면","insomnia.md"),
        @("소화불량","dyspepsia.md"),@("피로·기력저하 한약 처방 찾기","../herbal-integrated/formula-for-fatigue.md")
    )},
    @{File="conditions/dyspepsia.md"; Links=@(
        @("맞춤한약","custom-herbal-medicine.md"),@("만성피로","chronic-fatigue.md"),
        @("소화불량 한약 처방 찾기","../herbal-integrated/formula-for-digestion.md"),
        @("소화·비위 본초 찾기","../herbal-integrated/herbs-for-digestion.md"),
        @("소화불량과 경혈 찾기","../acupuncture-integrated/points-for-digestion.md")
    )},
    @{File="conditions/insomnia.md"; Links=@(
        @("만성피로","chronic-fatigue.md"),@("맞춤한약","custom-herbal-medicine.md"),
        @("불면 한약 처방 찾기","../herbal-integrated/formula-for-insomnia.md"),
        @("불면·심계 본초 찾기","../herbal-integrated/herbs-for-sleep.md"),
        @("불면과 경혈 찾기","../acupuncture-integrated/points-for-insomnia.md")
    )},
    @{File="conditions/low-back-pain.md"; Links=@(
        @("오래 앉으면 허리가 아파요","low-back-pain-sitting.md"),
        @("운전하면 목·허리가 아파요","driving-neck-back-pain.md"),
        @("근골격 통증 한약 처방 찾기","../herbal-integrated/formula-for-pain.md"),
        @("허리통증·요통과 경혈 찾기","../acupuncture-integrated/points-for-low-back.md"),
        @("근골격 통증 핵심","../acupuncture-integrated/musculoskeletal.md")
    )},
    @{File="conditions/shoulder-pain.md"; Links=@(
        @("팔을 위로 들면 어깨가 아파요","overhead-shoulder-pain.md"),
        @("컴퓨터 하면 목·어깨가 뭉쳐요","computer-neck-shoulder.md"),
        @("목·어깨 뭉침과 경혈 찾기","../acupuncture-integrated/points-for-neck-shoulder.md"),
        @("근골격 통증 핵심","../acupuncture-integrated/musculoskeletal.md"),
        @("약침치료","../acupuncture-integrated/pharmacopuncture.md")
    )}
)

$changed=0; $skipped=0
foreach($h in $Hubs){
    $p=Join-Path $Docs $h.File
    if(-not (Test-Path $p)){ Write-Host "SKIP missing: $($h.File)" -ForegroundColor Yellow; $skipped++; continue }
    $text=Get-Content $p -Raw -Encoding UTF8
    if($text.Contains($Marker)){ Write-Host "SKIP already linked: $($h.File)"; $skipped++; continue }

    $valid=@()
    foreach($pair in $h.Links){
        $label=$pair[0]; $target=$pair[1]
        $resolved=[System.IO.Path]::GetFullPath((Join-Path (Split-Path $p -Parent) $target))
        if(Test-Path $resolved){ $valid += ,@($label,$target) }
    }
    if($valid.Count -eq 0){ Write-Host "SKIP no valid links: $($h.File)" -ForegroundColor Yellow; $skipped++; continue }

    $backupFile=Join-Path $Backup $h.File
    New-Item -ItemType Directory -Force -Path (Split-Path $backupFile -Parent) | Out-Null
    Copy-Item $p $backupFile -Force

    $block="`r`n`r`n$Marker`r`n## 함께 보면 좋은 핵심 문서`r`n`r`n"
    foreach($v in $valid){ $block += "- [$($v[0])]($($v[1]))`r`n" }
    Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
    Write-Host "LINKED: $($h.File) ($($valid.Count))" -ForegroundColor Green
    $changed++
}
Write-Host ""
Write-Host "STEP 1 완료: 핵심 허브 $changed 개 보강 / $skipped 개 건너뜀" -ForegroundColor Cyan
Write-Host "원본 백업: HUB_LINK_BACKUP_STEP1"
Read-Host "Enter를 누르면 종료합니다"
