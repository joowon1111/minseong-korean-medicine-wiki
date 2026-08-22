$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_final07_"+$stamp
New-Item -ItemType Directory -Force $bk|Out-Null
$changedLinks=0;$changedMeta=0

# 1) Exact residual broken-link repair.
$map=@{
"sasang-symptoms/"="sasang-symptoms/index.md";
"../herbs/"="../herbs/index.md";
"../formulas/"="../formulas/index.md";
"../conditions/leg-numbness.md"="../conditions/foot-numbness.md";
"../conditions/hand-numbness.md"="../conditions/arm-numbness.md";
"../conditions/pediatric-tonic.md"="../conditions/child-parent-tonic-guide.md";
"../conditions/palpitations.md"="../conditions/palpitation.md";
"../conditions/plantar-fascia-pain.md"="../conditions/plantar-fasciitis.md";
"../conditions/chronic-pain.md"="../conditions/chronic-prostatitis.md"
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File|ForEach-Object{
 $t=Get-Content $_.FullName -Raw -Encoding UTF8;$o=$t
 foreach($k in $map.Keys){$t=$t.Replace("("+$k+")","("+$map[$k]+")")}
 if($t -ne $o){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $dest=Join-Path $bk $rel;$dd=Split-Path $dest -Parent;if(-not(Test-Path $dd)){New-Item -ItemType Directory -Force $dd|Out-Null}
  Copy-Item $_.FullName $dest -Force;Set-Content $_.FullName $t -Encoding UTF8;$changedLinks++
 }
}

# 2) Re-apply priority metadata directly, without TSV/Import-Csv dependency.
$paths=Get-Content "priority_metadata_paths.txt" -Encoding UTF8
foreach($r in $paths){
 if([string]::IsNullOrWhiteSpace($r)){continue}
 $p=Join-Path "docs" ($r.Replace("/","\"))
 if(-not(Test-Path $p)){continue}
 $t=Get-Content $p -Raw -Encoding UTF8
 if($t.StartsWith("---")){continue}
 $m=[regex]::Match($t,'(?m)^#\s+(.+?)\s*$')
 if($m.Success){$title=$m.Groups[1].Value.Trim()}else{$title=[IO.Path]::GetFileNameWithoutExtension($p).Replace("-"," ")}
 $title=$title.Replace('"','')
 if($r.StartsWith("conditions/")){
  $desc=$title+"의 주요 증상과 감별, 한의학적 해석, 치료 접근과 관련 정보를 정리한 민성 한의학 아카이브 문서입니다."
  $tags=@("증상질환","환자검색","한의학","AEO")
 }elseif($r.StartsWith("formulas/")){
  $desc=$title+"의 출전과 구성, 방의, 전통적 활용, 현대 연구와 임상적 해석을 정리한 방제 문서입니다."
  $tags=@("방제","처방","한약","현대연구")
 }else{
  $desc=$title+"의 기원과 성미·귀경, 전통 효능, 주요 처방에서의 역할과 현대 연구를 정리한 본초 문서입니다."
  $tags=@("본초","한약재","효능","현대연구")
 }
 $tagtext=($tags|ForEach-Object{"  - "+$_}) -join "`r`n"
 $fm="---`r`ntitle: `"$title`"`r`ndescription: `"$desc`"`r`ntags:`r`n$tagtext`r`n---`r`n`r`n"
 $rel=$r.Replace("/","\");$dest=Join-Path $bk $rel;$dd=Split-Path $dest -Parent
 if(-not(Test-Path $dd)){New-Item -ItemType Directory -Force $dd|Out-Null}
 if(-not(Test-Path $dest)){Copy-Item $p $dest -Force}
 Set-Content $p ($fm+$t) -Encoding UTF8;$changedMeta++
}
Write-Host ("FINAL QUALITY FIX 07 COMPLETE") -ForegroundColor Green
Write-Host ("Link files repaired: "+$changedLinks) -ForegroundColor Green
Write-Host ("Priority metadata added: "+$changedMeta) -ForegroundColor Green
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
