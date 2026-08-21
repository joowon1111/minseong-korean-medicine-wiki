$ErrorActionPreference="Stop"
try {
  $Root=Split-Path -Parent $MyInvocation.MyCommand.Path
  Set-Location $Root
  $Docs=Join-Path $Root "docs"
  if(-not(Test-Path $Docs)){throw "docs folder not found"}

  $Backup=Join-Path $Root "FINAL_RESIDUAL_BACKUP"
  New-Item -ItemType Directory -Force -Path $Backup | Out-Null
  $Report=Join-Path $Root "FINAL_RESIDUAL_REPORT.md"
  $Marker="<!-- MINSEONG_FINAL_RESIDUAL_V1 -->"

  function DocRel($p){
    $du=New-Object System.Uri(($Docs.TrimEnd('\')+'\'))
    $fu=New-Object System.Uri($p)
    return [Uri]::UnescapeDataString($du.MakeRelativeUri($fu).ToString())
  }
  function RelLink($from,$to){
    $fu=New-Object System.Uri(((Split-Path -Parent $from).TrimEnd('\')+'\'))
    $tu=New-Object System.Uri($to)
    return [Uri]::UnescapeDataString($fu.MakeRelativeUri($tu).ToString())
  }
  function HasDesc($t){return $t -match '(?m)^description:\s*\S+'}
  function CountLinks($t){
    $n=0
    foreach($m in [regex]::Matches($t,'\[[^\]]+\]\(([^)]+)\)')){
      if($m.Groups[1].Value -notmatch '^(https?:|mailto:|#)'){$n++}
    }
    return $n
  }
  function GetTitle($t,$f){
    if($t -match '(?m)^title:\s*(.+?)\s*$'){return $Matches[1].Trim().Trim('"').Trim("'")}
    if($t -match '(?m)^#\s+(.+?)\s*$'){return $Matches[1].Trim()}
    return $f
  }
  function AddDesc($t,$d){
    if(HasDesc $t){return $t}
    if($t -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
      $fm=$Matches[1].TrimEnd()+"`r`ndescription: $d"
      return [regex]::Replace($t,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
    }
    return "---`r`ndescription: $d`r`n---`r`n"+$t
  }
  function BackupFile($p,$rel){
    $b=Join-Path $Backup $rel.Replace('/','\')
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $b)|Out-Null
    Copy-Item $p $b -Force
  }

  $files=Get-ChildItem $Docs -Recurse -File -Filter *.md
  $descBefore=@()
  $linkBefore=@()
  foreach($p in $files){
    $t=Get-Content $p.FullName -Raw -Encoding UTF8
    if(-not(HasDesc $t)){$descBefore+=$p}
    if((CountLinks $t)-lt 3){$linkBefore+=$p}
  }

  # Residuals that are intentionally allowed to stay short/unlinked.
  $IntentionalRegex='(^|/)(templates?)(/|$)|(^|/)(references|citation-policy|status-policy|clinical-template)\.md$'

  $fixed=0
  $intentional=@()
  $targets=@{}
  foreach($p in $descBefore){$targets[$p.FullName]=$p}
  foreach($p in $linkBefore){$targets[$p.FullName]=$p}

  foreach($p in $targets.Values){
    $rel=DocRel $p.FullName
    if($rel -match $IntentionalRegex){
      $intentional += $rel
      continue
    }
    $t=Get-Content $p.FullName -Raw -Encoding UTF8
    $orig=$t
    $title=GetTitle $t $p.BaseName

    if(-not(HasDesc $t)){
      $t=AddDesc $t "$title — 민성 한의학 아카이브의 관련 전문 지식과 핵심 허브를 연결하는 문서입니다."
    }

    if((CountLinks $t)-lt 3 -and -not $t.Contains($Marker)){
      $candidates=@(
        @("아카이브 안내","guide/index.md"),
        @("증상·질환","conditions/index.md"),
        @("본초·방제","herbal-integrated/index.md"),
        @("침구·치료","acupuncture-integrated/index.md"),
        @("연구·근거","evidence-integrated/index.md")
      )
      $valid=@()
      foreach($x in $candidates){
        $dest=Join-Path $Docs $x[1].Replace('/','\')
        if(Test-Path $dest){
          if((Resolve-Path $dest).Path -ne (Resolve-Path $p.FullName).Path){
            $valid+=,@($x[0],(RelLink $p.FullName (Resolve-Path $dest).Path))
          }
        }
        if($valid.Count -ge 3){break}
      }
      if($valid.Count -gt 0){
        $block="`r`n`r`n$Marker`r`n## 관련 핵심 허브`r`n`r`n"
        foreach($v in $valid){$block+="- [$($v[0])]($($v[1]))`r`n"}
        $t=$t.TrimEnd()+$block
      }
    }

    if($t -ne $orig){
      BackupFile $p.FullName $rel
      Set-Content $p.FullName $t -Encoding UTF8
      $fixed++
    }
  }

  $descAfter=@();$linkAfter=@()
  foreach($p in Get-ChildItem $Docs -Recurse -File -Filter *.md){
    $t=Get-Content $p.FullName -Raw -Encoding UTF8
    if(-not(HasDesc $t)){$descAfter+=DocRel $p.FullName}
    if((CountLinks $t)-lt 3){$linkAfter+=DocRel $p.FullName}
  }

  $r=@()
  $r+="# Final Residual Cleanup Report"
  $r+=""
  $r+="## Result"
  $r+="- Fixed residual content files: **$fixed**"
  $r+="- Missing descriptions: **$($descBefore.Count) -> $($descAfter.Count)**"
  $r+="- Fewer than 3 internal links: **$($linkBefore.Count) -> $($linkAfter.Count)**"
  $r+=""
  $r+="## Remaining description exceptions"
  if($descAfter.Count){foreach($x in $descAfter){$r+="- ``$x``"}}else{$r+="- None"}
  $r+=""
  $r+="## Remaining link exceptions"
  if($linkAfter.Count){foreach($x in $linkAfter){$r+="- ``$x``"}}else{$r+="- None"}
  $r+=""
  $r+="Remaining template/reference/policy files may be intentional exceptions and do not need artificial content inflation."
  $r | Set-Content $Report -Encoding UTF8

  Write-Host ""
  Write-Host "==============================================" -ForegroundColor Green
  Write-Host "FINAL RESIDUAL CLEANUP COMPLETE" -ForegroundColor Green
  Write-Host "==============================================" -ForegroundColor Green
  Write-Host "Fixed files: $fixed"
  Write-Host "Missing descriptions: $($descBefore.Count) -> $($descAfter.Count)" -ForegroundColor Cyan
  Write-Host "Low internal links: $($linkBefore.Count) -> $($linkAfter.Count)" -ForegroundColor Cyan
  Write-Host "Report: FINAL_RESIDUAL_REPORT.md"
}
catch{
  Write-Host ""
  Write-Host "ERROR" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  ($_|Out-String)|Set-Content (Join-Path $Root "FINAL_RESIDUAL_ERROR.txt") -Encoding UTF8
}
Write-Host ""
Read-Host "Press Enter to close"
