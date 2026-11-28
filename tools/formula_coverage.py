"""Count exact core-list documents separately from source-qualified variants."""
from collections import defaultdict
from html import escape
import re
from urllib.parse import unquote, urlsplit
from ontology import BASE, source_url, visible_source

FORMULARY = 'herbal-integrated/general-formulary.md'
MARKER = '<!-- MINSEONG_ONTOLOGY_CORE_FORMULA_COVERAGE -->'


def core_entries(docs):
    text = visible_source(docs / FORMULARY)
    start = re.search(r'^## [^\n]*\{#core-formulas-100\}[^\n]*\n', text, re.M)
    if not start:
        raise ValueError('Missing core-formulas-100 section')
    section = re.split(r'^## ', text[start.end():], maxsplit=1, flags=re.M)[0]
    group = None
    entries = []
    for line in section.splitlines():
        if line.startswith('### '):
            group = re.sub(r'\s*\{#[^}]+\}', '', line[4:]).strip()
        match = re.match(r'^\| \[([^]]+)]\(([^)]+)\)', line)
        if not match:
            continue
        label, target = match.groups()
        parts = urlsplit(target)
        path = ((docs / FORMULARY).parent / unquote(parts.path)).resolve()
        if parts.scheme or parts.netloc or parts.query or parts.fragment:
            raise ValueError('Core formula must link directly to a local document')
        if not path.is_relative_to(docs.resolve() / 'formulas') or not path.is_file():
            raise ValueError('Invalid core formula document: ' + target)
        relative = path.relative_to(docs.resolve()).as_posix()
        if not group:
            raise ValueError('Core formula has no clinical group')
        entries.append(dict(label=label, page=relative, url=source_url(relative, docs), group=group))
    if len(entries) != 100 or len({e['page'] for e in entries}) != 100 or len({e['label'] for e in entries}) != 100:
        raise ValueError('Core list must contain 100 distinct formula documents and labels')
    return entries


def formula_coverage(payload, docs):
    """Membership comes only from explicit containsHerb, matched by document URL."""
    nodes = {n['@id']: n for n in payload['@graph']}
    herbs = defaultdict(set)
    sources = defaultdict(set)
    for n in nodes.values():
        if n.get('@type') == 'rdf:Statement' and n['rdf:predicate']['@id'] == 'km:containsHerb':
            fid, hid = n['rdf:subject']['@id'], n['rdf:object']['@id']
            if 'km:Formula' not in nodes[fid]['@type'] or 'km:Herb' not in nodes[hid]['@type']:
                raise ValueError('Invalid composition coverage types')
            herbs[fid].add(hid)
            sources[fid].add(n['dcterms:source']['@id'])
    by_page = defaultdict(list)
    for fid in sorted(herbs):
        n = nodes[fid]
        by_page[n['foaf:page']['@id'].split('#', 1)[0]].append(dict(
            id=fid, label=n['skos:prefLabel']['@value'], url=n['foaf:page']['@id'],
            herb_count=len(herbs[fid]), sources=sorted(sources[fid])))
    entries = core_entries(docs)
    for e in entries:
        e['variants'] = by_page.get(e['url'], [])
        e['has_composition_records'] = bool(e['variants'])
    core_urls = {e['url'] for e in entries}
    outside = [dict(url=url, variants=variants) for url, variants in sorted(by_page.items()) if url not in core_urls]
    count = sum(e['has_composition_records'] for e in entries)
    return dict(schema_version=1, source=source_url(FORMULARY+'#core-formulas-100', docs),
                counting_rule='Exact document URLs; explicit containsHerb statements only. Registration does not establish composition completeness or clinical efficacy.',
                summary=dict(core_total=len(entries), core_registered=count, core_pending=len(entries)-count,
                             all_registered_documents=len(by_page), other_registered_documents=len(outside),
                             registered_variants=len(herbs)),
                core=entries, other_registered=outside)


def coverage_markdown(report):
    def link(label, url):
        label = escape(label)
        for character in '|[]*_`\\':
            label = label.replace(character, '&#' + str(ord(character)) + ';')
        return '<a href="' + escape(url, quote=True) + '">' + label + '</a>'
    s = report['summary']
    lines = [f"핵심 100선 중 **{s['core_registered']}/{s['core_total']}개** 문서에 구성 관계가 등록되어 있습니다. 전체 등록 처방 문서는 **{s['all_registered_documents']}개**이며, 이 중 **{s['other_registered_documents']}개**는 100선 밖의 연관 처방입니다. 같은 문서의 여러 수록형은 처방 문서 수에서 한 번만 셉니다.", '',
             '등록 표시는 출전이 명시된 구성 관계가 있다는 뜻입니다. 기본 약미·포제·전탕 추가재료와 등록 범위는 각 수록형의 구성 출처에서 확인합니다.', '',
             '| 처방군 | 구성 등록 / 전체 | 등록된 처방·수록형 | 구성 관계 대기 처방 |', '|---|---:|---|---|']
    groups = defaultdict(list)
    for e in report['core']:
        groups[e['group']].append(e)
    for group, entries in groups.items():
        registered, pending = [], []
        for e in entries:
            if e['has_composition_records']:
                variants = ' · '.join(link(v['label'], v['url']) for v in e['variants'])
                registered.append(variants)
            else:
                pending.append(link(e['label'], e['url']))
        def details(label, values):
            return '<details><summary>'+label+'</summary>'+'<br>'.join(values)+'</details>' if values else '—'
        lines.append('| '+link(group, report['source'])+' | '+str(sum(e['has_composition_records'] for e in entries))+' / '+str(len(entries))+' | '+details('등록 수록형 보기',registered)+' | '+details('대기 처방 보기',pending)+' |')
    lines += ['', link('전체 구성 관계·수록형 비교', BASE+'/network/#ontology-composition-tables')+' · '+link('등록 현황 데이터', BASE+'/assets/ai/core-formula-coverage.json'), '']
    return '\n'.join(lines)
