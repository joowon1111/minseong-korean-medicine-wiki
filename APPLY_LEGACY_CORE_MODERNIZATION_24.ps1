$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs")){throw "docs folder not found"}
$bk="_backup_legacy_modernization24_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null

$targets=@(
"docs\pillar\index.md","docs\pillar\pain-musculoskeletal.md","docs\pillar\digestion-spleen-stomach.md",
"docs\pillar\sleep-neuro.md","docs\pillar\acupuncture-treatment.md","docs\pillar\clinical-evidence.md",
"docs\sasang\index.md","docs\sasang\soyangin.md","docs\sasang\soeumin.md","docs\sasang\taeeumin.md","docs\sasang\taeyangin.md",
"docs\formula-architecture\index.md","docs\research\index.md","docs\network\acupuncture-clinical-map.md"
)

foreach($t in $targets){
 if(Test-Path $t){
  $safe=$t.Replace("\","_")
  Copy-Item $t (Join-Path $bk $safe) -Force
 }
 $src=Join-Path "_payload" $t
 if(!(Test-Path $src)){throw ("payload missing: "+$src)}
 Copy-Item $src $t -Force
}

New-Item -ItemType Directory -Force "_legacy_modernization"|Out-Null
Copy-Item "_payload\_legacy_modernization\LEGACY_MODERNIZATION_REPORT.md" "_legacy_modernization\LEGACY_MODERNIZATION_REPORT.md" -Force

Write-Host "LEGACY CORE MODERNIZATION 24 COMPLETE" -ForegroundColor Green
Write-Host "14 early core pages were integrated and rebuilt, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
