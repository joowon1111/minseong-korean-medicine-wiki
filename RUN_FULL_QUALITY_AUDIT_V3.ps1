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

    function RelPath($full){
        $r=$full.Substring($docsRoot.Length)
        $r=$r.TrimStart([char[]]"\/")
        return $r.Replace('\','/')
    }

    foreach($f in $files){
        $rel=RelPath $f.FullName
        $existing[$rel]=$true
    }

    $incoming=@{}
    $broken=@()
    $noFront=@()
    $noH1=@()
    $thin=@()
    $answers=@()
    $noCore=@()
    $titleMap=@{}
    $descMap=@{}
    $answerTitles=@{}

    function AddMapValue($map,$key,$val){
        if([string]::IsNullOrWhiteSpace($key)){return}
        if(-not $map.ContainsKey($key)){ $map[$key]=@() }
        $map[$key]=@($map[$key]) + $val
    }

    foreach($f in $files){
        $rel=RelPath $f.FullName
        $text=Get-Content $f.FullName -Raw -Encoding UTF8

        $hasFront=$text.StartsWith("---")
        if(-not $hasFront){$noFront += $rel}

        $title=""
        $desc=""
        if($hasFront){
            $front=""
            if($text -match '(?s)^---\s*(.*?)\s*---'){ $front=$matches[1] }
            if($front -match '(?m)^title:\s*["'']?(.*?)["'']?\s*$'){ $title=$matches[1].Trim() }
            if($front -match '(?m)^description:\s*["'']?(.*?)["'']?\s*$'){ $desc=$matches[1].Trim() }
        }
        AddMapValue $titleMap $title $rel
        AddMapValue $descMap $desc $rel

        if($text -notmatch '(?m)^#\s+\S'){ $noH1 += $rel }
        $plain=($text -replace '\s+',' ')
        if($plain.Length -lt 650){ $thin += $rel }

        if($rel.StartsWith("answer-guides/")){
            $answers += $rel
            $answerTitles[$rel]=$title
            if($text -notmatch '(?m)^##\s+핵심 답변\s*$'){ $noCore += $rel }
        }

        foreach($m in [regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')){
            $target=$m.Groups[1].Value.Trim()
            if([string]::IsNullOrWhiteSpace($target)){continue}
            if($target.StartsWith("http://") -or $target.StartsWith("https://") -or $target.StartsWith("mailto:") -or $target.StartsWith("#")){continue}

            $target=($target -split '#')[0]
            $target=($target -split '\?')[0]
            if([string]::IsNullOrWhiteSpace($target)){continue}

            try{
                $base=Split-Path $f.FullName -Parent
                $candidate=[System.IO.Path]::GetFullPath((Join-Path $base $target))
                if(-not $candidate.StartsWith($docsRoot,[System.StringComparison]::OrdinalIgnoreCase)){continue}
                $tr=RelPath $candidate
                if($tr.EndsWith("/")){$tr+="index.md"}
                if(-not $tr.EndsWith(".md")){$tr+=".md"}

                if($existing.ContainsKey($tr)){
                    if(-not $incoming.ContainsKey($tr)){$incoming[$tr]=0}
                    $incoming[$tr]=[int]$incoming[$tr]+1
                } else {
                    $broken += [pscustomobject]@{source=$rel; target=$target; resolved=$tr}
                }
            } catch {}
        }
    }

    $nav=@{}
    if(Test-Path "mkdocs.yml"){
        $yml=Get-Content "mkdocs.yml" -Raw -Encoding UTF8
        foreach($m in [regex]::Matches($yml,'(?m)([A-Za-z0-9_./-]+\.md)\s*$')){
            $nav[$m.Groups[1].Value]=$true
        }
    }

    $notInNav=@()
    $orphans=@()
    foreach($r in $existing.Keys){
        if(-not $nav.ContainsKey($r)){ $notInNav += $r }
        $inc=0
        if($incoming.ContainsKey($r)){$inc=[int]$incoming[$r]}
        if($inc -eq 0 -and -not $nav.ContainsKey($r) -and -not $r.EndsWith("index.md")){
            $orphans += $r
        }
    }

    $dupTitles=@()
    foreach($k in $titleMap.Keys){
        if(@($titleMap[$k]).Count -gt 1){
            $dupTitles += [pscustomobject]@{title=$k; files=@($titleMap[$k])}
        }
    }
    $dupDescs=@()
    foreach($k in $descMap.Keys){
        if(@($descMap[$k]).Count -gt 1){
            $dupDescs += [pscustomobject]@{description=$k; files=@($descMap[$k])}
        }
    }

    function Tokens($s){
        if([string]::IsNullOrWhiteSpace($s)){return @()}
        return @([regex]::Matches($s.ToLower(),'[가-힣a-z0-9]{2,}') | ForEach-Object {$_.Value} | Sort-Object -Unique)
    }

    $sim=@()
    $alist=@($answers | Sort-Object)
    for($i=0;$i -lt $alist.Count;$i++){
        $a=$alist[$i]; $A=Tokens $answerTitles[$a]
        for($j=$i+1;$j -lt $alist.Count;$j++){
            $b=$alist[$j]; $B=Tokens $answerTitles[$b]
            if($A.Count -eq 0 -or $B.Count -eq 0){continue}
            $union=@($A+$B | Sort-Object -Unique)
            $inter=@($A | Where-Object {$B -contains $_})
            $score=[math]::Round(($inter.Count/[math]::Max(1,$union.Count)),3)
            if($score -ge 0.50){
                $sim += [pscustomobject]@{score=$score; a=$a; b=$b}
            }
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

    function AddSection($name,$items,$kind){
        [void]$sb.AppendLine("## $name")
        [void]$sb.AppendLine("")
        if(@($items).Count -eq 0){
            [void]$sb.AppendLine("- 없음")
            [void]$sb.AppendLine("")
            return
        }
        $c=0
        foreach($x in @($items)){
            if($c -ge 300){[void]$sb.AppendLine("- … 나머지 생략"); break}
            if($kind -eq "broken"){ $line="$($x.source) → $($x.target) (resolved: $($x.resolved))" }
            elseif($kind -eq "sim"){ $line="$($x.score) | $($x.a) ↔ $($x.b)" }
            else { $line="$x" }
            [void]$sb.AppendLine("- "+$line); $c++
        }
        [void]$sb.AppendLine("")
    }

    AddSection "깨진 내부링크" $broken "broken"
    AddSection "고아 페이지 후보" ($orphans|Sort-Object) "plain"
    AddSection "nav 미등록 문서" ($notInNav|Sort-Object) "plain"
    AddSection "front matter 없음" $noFront "plain"
    AddSection "H1 없음" $noH1 "plain"
    AddSection "핵심답변 없는 answer-guide" $noCore "plain"
    AddSection "얇은 페이지 후보" $thin "plain"
    AddSection "유사 answer-guide 후보" $sim "sim"

    [void]$sb.AppendLine("## 중복 title"); [void]$sb.AppendLine("")
    if($dupTitles.Count -eq 0){[void]$sb.AppendLine("- 없음")}
    else{foreach($x in $dupTitles){[void]$sb.AppendLine("- **$($x.title)**: $(@($x.files) -join ', ')")}}
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("## 중복 description"); [void]$sb.AppendLine("")
    if($dupDescs.Count -eq 0){[void]$sb.AppendLine("- 없음")}
    else{foreach($x in $dupDescs){[void]$sb.AppendLine("- $($x.description): $(@($x.files) -join ', ')")}}

    $sb.ToString() | Set-Content $report -Encoding UTF8
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
