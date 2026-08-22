$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs")){throw "docs not found"}
$bk="_backup_linkfix_special31_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null

# 1) Modernize special-point pages in place.
foreach($src in Get-ChildItem "_payload\docs\meridian-network\special-points" -File){
  $dest=Join-Path "docs\meridian-network\special-points" $src.Name
  if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ("special_"+$src.Name)) -Force}
  Copy-Item $src.FullName $dest -Force
}

# 2) Fix known broken links from Audit 30 by mapping them to existing modern hubs.
$replacements = @{
"../clinical-core/pathways/dyspepsia.md"="../conditions/dyspepsia.md";
"../clinical-core/pathways/fatigue-recovery.md"="../conditions/fatigue.md";
"../clinical-core/pathways/insomnia.md"="../conditions/insomnia.md";
"../clinical-core/pathways/knee-leg-pain.md"="../conditions/knee-pain.md";
"../clinical-core/pathways/low-back-pain.md"="../conditions/low-back-pain.md";
"../clinical-core/pathways/palpitations-autonomic.md"="../conditions/palpitation.md";
"../clinical-core/pathways/rhinitis-cough.md"="../conditions/allergic-rhinitis.md";
"../clinical-core/pathways/women-cold-blood.md"="../conditions/dysmenorrhea.md";
"../../clinical-core/pathways/dyspepsia.md"="../../conditions/dyspepsia.md";
"../../clinical-core/pathways/fatigue-recovery.md"="../../conditions/fatigue.md";
"../../clinical-core/pathways/insomnia.md"="../../conditions/insomnia.md";
"../../clinical-core/pathways/low-back-pain.md"="../../conditions/low-back-pain.md";
"../../clinical-core/pathways/women-cold-blood.md"="../../conditions/dysmenorrhea.md"
}

$targets = @(
"docs\acupoint-network\by-condition.md",
"docs\conditions\allergic-rhinitis.md","docs\conditions\dyspepsia.md","docs\conditions\fatigue.md",
"docs\conditions\insomnia.md","docs\conditions\knee-pain.md","docs\conditions\low-back-pain.md",
"docs\formula-architecture\insomnia-family.md","docs\formula-architecture\sijunzi-family.md",
"docs\formula-architecture\siwu-qi-blood-family.md","docs\formula-architecture\tonic-family.md",
"docs\formulas\categories\phlegm-qi-formulas.md","docs\formulas\categories\tonic-formulas.md",
"docs\formulas\categories\wind-damp-musculoskeletal.md","docs\herbs\categories\blood.md",
"docs\herbs\categories\calm-spirit.md","docs\herbs\categories\tonics.md",
"docs\network\acupoint-combinations.md","docs\network\formula-acupoint-combinations.md",
"docs\pillar\digestion-spleen-stomach.md","docs\pillar\pain-musculoskeletal.md","docs\pillar\sleep-neuro.md"
)

foreach($t in $targets){
 if(Test-Path $t){
  $txt=Get-Content $t -Raw -Encoding UTF8
  $old=$txt
  foreach($k in $replacements.Keys){$txt=$txt.Replace($k,$replacements[$k])}
  if($txt -ne $old){
    Copy-Item $t (Join-Path $bk ("link_"+($t.Replace("\","_")))) -Force
    Set-Content $t $txt -Encoding UTF8
  }
 }
}

# 3) Other broken-link fixes explicitly identified in Audit 30.
if(Test-Path "docs\diagnostics\patterns\blood-deficiency.md"){
 $t="docs\diagnostics\patterns\blood-deficiency.md";$txt=Get-Content $t -Raw -Encoding UTF8
 $txt=$txt.Replace("../../herbs/cnidium.md","../../herbs/ligusticum.md")
 Set-Content $t $txt -Encoding UTF8
}
if(Test-Path "docs\diagnostics\patterns\kidney-deficiency.md"){
 $t="docs\diagnostics\patterns\kidney-deficiency.md";$txt=Get-Content $t -Raw -Encoding UTF8
 $txt=$txt.Replace("../../formulas/liu-wei-di-huang-wan.md","../../formulas/index.md")
 Set-Content $t $txt -Encoding UTF8
}
if(Test-Path "docs\pillar\pain-musculoskeletal.md"){
 $t="docs\pillar\pain-musculoskeletal.md";$txt=Get-Content $t -Raw -Encoding UTF8
 $txt=$txt.Replace("../formulas/shaoyao-gancao-tang.md","../formulas/index.md")
 Set-Content $t $txt -Encoding UTF8
}
if(Test-Path "docs\index.md"){
 $t="docs\index.md";$txt=Get-Content $t -Raw -Encoding UTF8
 $txt=$txt.Replace("portal/conditions/","conditions/")
 Set-Content $t $txt -Encoding UTF8
}

# 4) Classics index had missing jingui target: remove broken direct link if file absent, preserve concept via classics hub text.
if((Test-Path "docs\classics\index.md") -and !(Test-Path "docs\classics\jingui-yaolue.md")){
 $t="docs\classics\index.md";$txt=Get-Content $t -Raw -Encoding UTF8
 $txt=$txt.Replace("[금궤요략](jingui-yaolue.md)","금궤요략")
 Set-Content $t $txt -Encoding UTF8
}

Write-Host "LINKFIX + SPECIAL POINT MODERNIZATION 31 COMPLETE" -ForegroundColor Green
Write-Host "Audit-30 broken clinical links repaired and special-point core pages rebuilt in place." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
