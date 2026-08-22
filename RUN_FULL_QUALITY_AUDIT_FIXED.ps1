$ErrorActionPreference="Stop"
try {
    $Root=Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $Root
    if(-not(Test-Path "docs")) { throw "docs folder not found. ZIP을 저장소 최상위에 풀어주세요." }

    $out="_quality_audit"
    New-Item -ItemType Directory -Force $out | Out-Null
    $log=Join-Path $out "AUDIT_DEBUG.txt"
    "Audit started: $(Get-Date)" | Set-Content $log -Encoding UTF8

    $docsRoot=(Resolve-Path "docs").Path
    $files=Get-ChildItem "docs" -Recurse -Filter "*.md" -File
    $existing=@{}
    foreach($f in $files){
        $rel=$f.FullName.Substring($docsRoot.Length).TrimStart('\','/').Replace('\','/')
        $existing[$rel]=$true
    }

    $incoming=@{}
    $broken=New-Object System.Collections.Generic.List[object]
    $noFront=New-Object System.Collections.Generic.List[string]
    $noH1=New-Object System.Collections.Generic.List[string]
    $thin=New-Object System.Collections.Generic.List[string]
    $answers=New-Object System.Collections.Generic.List[string]
    $noCore=New-Object System.Collections.Generic.List[string]
    $titleMap=@{}
    $descMap=@{}
    $answerTitles=@{}

    function Add-Map($map,$key,$val){
        if([string]::IsNullOrWhiteSpace($key)){return}
        if(-not $map.ContainsKey($key)){ $map[$key]=New-Object System.Collections.Generic.List[string] }
        $map[$key].Add($val)
    }

    foreach($f in $files){
        $rel=$f.FullName.Substring($docsRoot.Length).TrimStart('\','/').Replace('\','/')
        $text=Get-Content $f.FullName -Raw -Encoding UTF8

        $hasFront=$text.StartsWith("---")
        if(-not $hasFront){$noFront.Add($rel)}

        $title=""
        $desc=""
        if($hasFront){
            if($text -match '(?ms)^---\s*.*?^title:\s*["'']?(.*?)["'']?\s*$'){ $title=$matches[1].Trim() }
            if($text -match '(?ms)^---\s*.*?^description:\s*["'']?(.*?)["'']?\s*$'){ $desc=$matches[1].Trim() }
        }
        Add-Map $titleMap $title $rel
        Add-Map $descMap $desc $rel

        if($text -notmatch '(?m)^#\s+\S'){ $noH1.Add($rel) }
        $plain=($text -replace '\s+',' ')
        if($plain.Length -lt 650){ $thin.Add($rel) }

        if($rel.StartsWith("answer-guides/")){
            $answers.Add($rel)
            $answerTitles[$rel]=$title
            if($text -notmatch '(?m)^##\s+핵심 답변\s*$'){ $noCore.Add($rel) }
        }

        $matches=[regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')
        foreach($m in $matches){
            $target=$m.Groups[1].Value.Trim()
            if([string]::IsNullOrWhiteSpace($target)){continue}
            if($target.StartsWith("http://") -or $target.StartsWith("https://") -or $target.StartsWith("mailto:") -or $target.StartsWith("#")){continue}
            $target=($target -split '#')[0]
            $target=($target -split '\?')[0]
            if([string]::IsNullOrWhiteSpace($target)){continue}

            $base=Split-Path $f.FullName -Parent
            try{
                $candidate=[System.IO.Path]::GetFullPath((Join-Path $base $target))
                if(-not $candidate.StartsWith($docsRoot,[System.StringComparison]::OrdinalIgnoreCase)){continue}
                $tr=$candidate.Substring($docsRoot.Length).TrimStart('\','/').Replace('\','/')
                if($tr.EndsWith("/")){$tr+="index.md"}
                if(-not $tr.EndsWith(".md")){$tr+=".md"}
                if($existing.ContainsKey($tr)){
                    if(-not $incoming.ContainsKey($tr)){$incoming[$tr]=0}
                    $incoming[$tr]++
                } else {
                    $broken.Add([pscustomobject]@{source=$rel; target=$target; resolved=$tr})
                }
            } catch {}
        }
    }

    # nav paths: parse all *.md strings from mkdocs.yml without requiring PyYAML
    $nav=@{}
    if(Test-Path "mkdocs.yml"){
        $yml=Get-Content "mkdocs.yml" -Raw -Encoding UTF8
        foreach($m in [regex]::Matches($yml,'(?m)([A-Za-z0-9_./-]+\.md)\s*$')){
            $nav[$m.Groups[1].Value]=$true
        }
    }

    $notInNav=New-Object System.Collections.Generic.List[string]
    $orphans=New-Object System.Collections.Generic.List[string]
    foreach($r in $existing.Keys){
        if(-not $nav.ContainsKey($r)){ $notInNav.Add($r) }
        $inc=0;if($incoming.ContainsKey($r)){$inc=$incoming[$r]}
        if($inc -eq 0 -and -not $nav.ContainsKey($r) -and -not $r.EndsWith("index.md")){$orphans.Add($r)}
    }

    $dupTitles=@()
    foreach($k in $titleMap.Keys){if($titleMap[$k].Count -gt 1){$dupTitles += [pscustomobject]@{title=$k; files=@($titleMap[$k])}}}
    $dupDescs=@()
    foreach($k in $descMap.Keys){if($descMap[$k].Count -gt 1){$dupDescs += [pscustomobject]@{description=$k; files=@($descMap[$k])}}}

    # answer-guide title token similarity (safe heuristic)
    function Tokens($s){
        if([string]::IsNullOrWhiteSpace($s)){return @()}
        $a=[regex]::Matches($s.ToLower(),'[가-힣a-z0-9]{2,}') | ForEach-Object {$_.Value} | Sort-Object -Unique
        return @($a)
    }
    $sim=New-Object System.Collections.Generic.List[object]
    $alist=@($answers | Sort-Object)
    for($i=0;$i -lt $alist.Count;$i++){
        $a=$alist[$i];$A=Tokens $answerTitles[$a]
        for($j=$i+1;$j -lt $alist.Count;$j++){
            $b=$alist[$j];$B=Tokens $answerTitles[$b]
            if($A.Count -eq 0 -or $B.Count -eq 0){continue}
            $union=@($A+$B | Sort-Object -Unique)
            $inter=@($A | Where-Object {$B -contains $_})
            $score=[math]::Round($inter.Count/[math]::Max(1,$union.Count),3)
            if($score -ge 0.50){$sim.Add([pscustomobject]@{score=$score; a=$a; b=$b})}
        }
    }
    $sim=@($sim | Sort-Object score -Descending)

    $report=Join-Path $out "AUDIT_REPORT.md"
    $sb=New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("# 민성 한의학 아카이브 전체 품질감사")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("- 전체 Markdown: **$($files.Count)**")
    [void]$sb.AppendLine("- answer-guides: **$($answers.Count)**")
    [void]$sb.AppendLine("- 깨진 내부링크: **$($broken.Count)**")
    [void]$sb.AppendLine("- nav 미등록: **$($notInNav.Count)**")
    [void]$sb.AppendLine("- 고아 페이지 후보: **$($orphans.Count)**")
    [void]$sb.AppendLine("- front matter 없음: **$($noFront.Count)**")
    [void]$sb.AppendLine("- H1 없음: **$($noH1.Count)**")
    [void]$sb.AppendLine("- 얇은 페이지 후보: **$($thin.Count)**")
    [void]$sb.AppendLine("- 핵심답변 없는 answer-guide: **$($noCore.Count)**")
    [void]$sb.AppendLine("- 유사 질문 후보: **$($sim.Count)**")
    [void]$sb.AppendLine("")

    function Add-Section($name,$items,$formatter){
        [void]$sb.AppendLine("## $name");[void]$sb.AppendLine("")
        if($items.Count -eq 0){[void]$sb.AppendLine("- 없음");[void]$sb.AppendLine("");return}
        $c=0
        foreach($x in $items){
            if($c -ge 300){[void]$sb.AppendLine("- … 나머지 생략");break}
            [void]$sb.AppendLine("- "+(& $formatter $x));$c++
        }
        [void]$sb.AppendLine("")
    }

    Add-Section "깨진 내부링크" @($broken) {param($x) "$($x.source) → $($x.target) (resolved: $($x.resolved))"}
    Add-Section "고아 페이지 후보" @($orphans|Sort-Object) {param($x) "$x"}
    Add-Section "nav 미등록 문서" @($notInNav|Sort-Object) {param($x) "$x"}
    Add-Section "front matter 없음" @($noFront) {param($x) "$x"}
    Add-Section "H1 없음" @($noH1) {param($x) "$x"}
    Add-Section "핵심답변 없는 answer-guide" @($noCore) {param($x) "$x"}
    Add-Section "얇은 페이지 후보" @($thin) {param($x) "$x"}
    Add-Section "유사 answer-guide 후보" @($sim) {param($x) "$($x.score) | $($x.a) ↔ $($x.b)"}

    [void]$sb.AppendLine("## 중복 title");[void]$sb.AppendLine("")
    if($dupTitles.Count -eq 0){[void]$sb.AppendLine("- 없음")} else {
        foreach($x in $dupTitles){[void]$sb.AppendLine("- **$($x.title)**: $($x.files -join ', ')")}
    }
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("## 중복 description");[void]$sb.AppendLine("")
    if($dupDescs.Count -eq 0){[void]$sb.AppendLine("- 없음")} else {
        foreach($x in $dupDescs){[void]$sb.AppendLine("- $($x.description): $($x.files -join ', ')")}
    }

    $sb.ToString() | Set-Content $report -Encoding UTF8

    # CSV summaries
    @($broken) | Export-Csv (Join-Path $out "broken_links.csv") -NoTypeInformation -Encoding UTF8
    @($sim) | Export-Csv (Join-Path $out "similar_answer_guides.csv") -NoTypeInformation -Encoding UTF8

    "SUCCESS`nMarkdown=$($files.Count)`nAnswerGuides=$($answers.Count)`nBroken=$($broken.Count)`nOrphans=$($orphans.Count)`nSimilar=$($sim.Count)" | Add-Content $log -Encoding UTF8

    Write-Host ""
    Write-Host "QUALITY AUDIT SUCCESS" -ForegroundColor Green
    Write-Host "Report: _quality_audit\AUDIT_REPORT.md" -ForegroundColor Cyan
    Write-Host "No site content was modified." -ForegroundColor Yellow
}
catch {
    $msg="ERROR: "+$_.Exception.Message
    Write-Host $msg -ForegroundColor Red
    New-Item -ItemType Directory -Force "_quality_audit" | Out-Null
    $msg | Set-Content "_quality_audit\AUDIT_DEBUG.txt" -Encoding UTF8
}
Read-Host "Press Enter to close"
