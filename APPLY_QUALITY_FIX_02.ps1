$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_quality_fix_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
$changed=0
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/autonomic-dysfunction.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/autonomic-dysfunction.md","../autonomic/index.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/prostate-urinary.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/prostate-urinary.md","../conditions/prostate-urinary-symptoms.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/womens-lifecycle.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/womens-lifecycle.md","../answer-guides/women-lifecycle-guide.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/anorexia.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/anorexia.md","../conditions/poor-appetite-adult.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/globus-sensation.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/globus-sensation.md","../conditions/globus.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/palpitations.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/palpitations.md","../conditions/palpitation.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/plantar-fascia-pain.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/plantar-fascia-pain.md","../conditions/plantar-fasciitis.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/hand-numbness.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/hand-numbness.md","../conditions/arm-numbness.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/leg-numbness.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/leg-numbness.md","../conditions/foot-numbness.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object {
 $t=Get-Content $_.FullName -Raw -Encoding UTF8
 if($t.Contains("../conditions/pediatric-tonic.md")){
  $rel=$_.FullName.Substring((Resolve-Path "docs").Path.Length).TrimStart([char]92)
  $bd=Join-Path $bk (Split-Path $rel -Parent); if($bd -and -not(Test-Path $bd)){New-Item -ItemType Directory -Force $bd|Out-Null}
  Copy-Item $_.FullName (Join-Path $bk $rel) -Force
  $t=$t.Replace("../conditions/pediatric-tonic.md","../answer-guides/when-child-tonic-guide.md")
  Set-Content $_.FullName $t -Encoding UTF8; $changed++
 }
}
# fix directory links detected in old docs
Get-ChildItem "docs" -Recurse -Filter "*.md" -File | ForEach-Object { $t=Get-Content $_.FullName -Raw -Encoding UTF8; $o=$t; $t=$t.Replace("../herbs/","../herbs/index.md").Replace("../formulas/","../formulas/index.md"); if($t -ne $o){Set-Content $_.FullName $t -Encoding UTF8;$changed++}}
Write-Host ("SAFE LINK REPAIR COMPLETE. Changed occurrences/files: "+$changed) -ForegroundColor Green
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"