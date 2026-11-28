"""Render source-qualified composition relations in the existing network page."""
from collections import defaultdict
from functools import lru_cache
from html import escape
from pathlib import Path

from ontology import BASE, build_ontology

MARKER = '<!-- MINSEONG_ONTOLOGY_COMPOSITION_TABLES -->'
HERB_MARKER = '<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->'
MERIDIAN_MARKER = '<!-- MINSEONG_ONTOLOGY_MERIDIAN_MEMBERS -->'
CLASSICAL_MARKER = '<!-- MINSEONG_ONTOLOGY_CLASSICAL_FORMULAS -->'
VARIANT_MARKER = '<!-- MINSEONG_ONTOLOGY_VARIANT_COMPARISONS -->'
ROOT = Path(__file__).resolve().parents[1]


def link(label, url):
    # Literal labels in Markdown table cells, with only validated local URLs.
    label = escape(' '.join(label.splitlines()))
    for character in '|[]*_`\\':
        label = label.replace(character, '&#' + str(ord(character)) + ';')
    return '<a href="' + escape(url, quote=True) + '">' + label + '</a>'


def composition_tables(payload):
    """Project explicit containsHerb statements; never infer absent relations."""
    nodes = {node['@id']: node for node in payload['@graph']}
    formulas = defaultdict(set)
    sources = defaultdict(set)
    for node in payload['@graph']:
        if node['@type'] != 'rdf:Statement' or node['rdf:predicate']['@id'] != 'km:containsHerb':
            continue
        subject, target = node['rdf:subject']['@id'], node['rdf:object']['@id']
        if 'km:Formula' not in nodes[subject]['@type'] or 'km:Herb' not in nodes[target]['@type']:
            raise ValueError('Invalid composition view types')
        formulas[subject].add(target)
        sources[subject].add(node['dcterms:source']['@id'])

    def label(key):
        return nodes[key]['skos:prefLabel']['@value']

    def concept_link(key):
        return link(label(key), nodes[key]['foaf:page']['@id'])

    ordered = sorted(formulas, key=lambda key: (label(key), key))
    lines = ['### 수록형별 구성과 출처 {#ontology-formula-compositions}', '',
             '| 처방 수록형 | 등록된 구성 본초·보조재료 | 구성·조건의 출처 |',
             '|---|---|---|']
    for formula in ordered:
        herbs = ' · '.join(concept_link(herb) for herb in sorted(formulas[formula], key=lambda key: (label(key), key)))
        refs = sorted(sources[formula])
        source_links = ' · '.join(link('원문·구성 확인' if len(refs) == 1 else '출처 ' + str(i), url)
                                  for i, url in enumerate(refs, 1))
        lines.append('| ' + concept_link(formula) + ' | ' + herbs + ' | ' + source_links + ' |')
    lines += ['', '각 수록형의 원문 약량·포제와 전탕 추가재료는 구성 출처에서 확인합니다. 귀비탕·산조인탕·생맥산·경옥고의 여러 수록형은 이름과 출처를 각각 유지합니다. 작약·백작약, 복령·백복령·적복령·복신, 건지황·숙지황, 계지·계심·육계도 원문과 가공에 맞춰 구분합니다.', '',
              '### 본초에서 처방 찾아가기 {#ontology-shared-herbs}', '',
              '현재 구성 관계가 등록된 본초를 모두 표시합니다. 인삼·황기·당귀처럼 여러 처방에 들어가는 약재는 수록형별 전체 배합과 출처를 비교하고, 약용 부위·가공·원문 약명이 다른 항목은 각각 확인할 수 있습니다.', '',
              '| 본초 | 구성 관계가 등록된 처방 수록형 |', '|---|---|']
    inverse = defaultdict(set)
    for formula, herbs in formulas.items():
        for herb in herbs:
            inverse[herb].add(formula)
    for herb in sorted(inverse, key=lambda key: (label(key), key)):
        related = ' · '.join(concept_link(formula) for formula in sorted(inverse[herb], key=lambda key: (label(key), key)))
        lines.append('| ' + concept_link(herb) + ' | ' + related + ' |')
    return '\n'.join(lines) + '\n'


def herb_formula_table(payload, source_path):
    """Select concepts by their exact document URI, retaining part identities."""
    suffix = source_path[:-8] if source_path.endswith('/index.md') else source_path[:-3] + '/'
    canonical = BASE + '/' + suffix
    nodes = {node['@id']: node for node in payload['@graph']}
    herbs = {key for key, node in nodes.items()
             if 'km:Herb' in node.get('@type', [])
             and node['foaf:page']['@id'].split('#', 1)[0] == canonical}
    rows = defaultdict(set)
    for node in payload['@graph']:
        if (node['@type'] == 'rdf:Statement'
                and node['rdf:predicate']['@id'] == 'km:containsHerb'
                and node['rdf:object']['@id'] in herbs):
            rows[(node['rdf:object']['@id'], node['rdf:subject']['@id'],
                  node['dcterms:source']['@id'])].add(node['skos:scopeNote']['@value'])
    if not rows:
        raise ValueError('No explicit ontology composition records for ' + source_path)
    def label(key):
        return nodes[key]['skos:prefLabel']['@value']
    lines = ['| 원문 약명 | 처방 수록형 | 구성 출처·수록 조건 |', '|---|---|---|']
    for herb, formula, source in sorted(rows, key=lambda row: (label(row[0]), label(row[1]), row)):
        notes = ''.join('<p>' + escape(scope).replace('|', '&#124;').replace('\n', '<br>') + '</p>'
                        for scope in sorted(rows[(herb, formula, source)]))
        context = '<details class="ontology-herb-context"><summary>약량·포제·전탕 조건</summary>' + notes + '</details>'
        lines.append('| ' + link(label(herb), nodes[herb]['foaf:page']['@id'])
                     + ' | ' + link(label(formula), nodes[formula]['foaf:page']['@id'])
                     + ' | ' + link('원문·구성 확인', source) + context + ' |')
    lines += ['', '현재 온톨로지에 구성 관계가 등록된 수록형입니다. 각 행의 ‘약량·포제·전탕 조건’을 펼치면 기본 약미·전탕 추가재료와 수록량·가공에 관한 등록 기록을 볼 수 있습니다. 상세 원문은 구성 출처에서 확인합니다. '
              + link('전체 수록형의 구성 비교', BASE + '/network/#ontology-formula-compositions') + '에서도 이어 볼 수 있습니다.', '']
    return '\n'.join(lines)


def variant_comparisons(payload):
    """Compare explicit same-name pairs using their qualified ingredient records."""
    nodes = {node['@id']: node for node in payload['@graph']}
    ingredients = defaultdict(set)
    sources = defaultdict(set)
    records = defaultdict(lambda: defaultdict(set))
    pairs = defaultdict(set)
    for node in nodes.values():
        if node['@type'] != 'rdf:Statement':
            continue
        subject, target = node['rdf:subject']['@id'], node['rdf:object']['@id']
        predicate = node['rdf:predicate']['@id']
        if predicate == 'km:containsHerb':
            ingredients[subject].add(target)
            sources[subject].add(node['dcterms:source']['@id'])
            records[subject][target].add((node['dcterms:source']['@id'], node['skos:scopeNote']['@value']))
        elif predicate == 'km:sharesNameWith':
            if any('km:Formula' not in nodes[key]['@type'] for key in (subject, target)):
                raise ValueError('Invalid formula variant view types')
            pairs[tuple(sorted((subject, target)))].add(
                (node['dcterms:source']['@id'], node['skos:scopeNote']['@value']))

    def label(key):
        return nodes[key]['skos:prefLabel']['@value']

    def herb_links(keys):
        return ' · '.join(link(label(key), nodes[key]['foaf:page']['@id'])
                          for key in sorted(keys, key=lambda key: (label(key), key))) or '—'

    lines = []
    for pair in sorted(pairs, key=lambda pair: (label(pair[0]), label(pair[1]), pair)):
        first, second = pair
        if not ingredients[first] or not ingredients[second]:
            raise ValueError('Variant comparison requires registered ingredients')
        common = ingredients[first] & ingredients[second]
        lines += ['<details class="ontology-variant-comparison">',
                  '<summary>' + escape(label(first) + ' ↔ ' + label(second)) + '</summary>',
                  '<p><strong>공통으로 등록된 본초 (' + str(len(common)) + ')</strong><br>'
                  + herb_links(common) + '</p>',
                  '<table><thead><tr><th>수록형</th><th>한쪽에만 등록된 본초</th>'
                  '<th>수록형의 정의·구성 출처</th></tr></thead><tbody>']
        for key, other in [(first, second), (second, first)]:
            refs = ' · '.join(link('구성 출처 ' + str(i), url)
                              for i, url in enumerate(sorted(sources[key]), 1))
            lines.append('<tr><td>' + link(label(key), nodes[key]['foaf:page']['@id'])
                         + '</td><td>' + herb_links(ingredients[key] - ingredients[other])
                         + '</td><td>' + escape(nodes[key]['skos:definition']['@value'])
                         + '<br>' + refs + '</td></tr>')
        lines.append('</tbody></table>')
        lines += ['<details class="ontology-variant-records"><summary>약미별 수록 조건·출처</summary>',
                  '<table><thead><tr><th>등록된 본초</th><th>' + escape(label(first))
                  + '</th><th>' + escape(label(second)) + '</th></tr></thead><tbody>']
        for herb in sorted(ingredients[first] | ingredients[second], key=lambda key: (label(key), key)):
            cells = []
            for formula in pair:
                notes = ''.join('<p>' + escape(scope) + ' ' + link('구성 근거', source) + '</p>'
                                for source, scope in sorted(records[formula][herb]))
                cells.append('<td>' + (notes or '—') + '</td>')
            lines.append('<tr><td>' + link(label(herb), nodes[herb]['foaf:page']['@id'])
                         + '</td>' + ''.join(cells) + '</tr>')
        lines.append('</tbody></table></details>')
        for source, scope in sorted(pairs[pair]):
            lines.append('<p><strong>비교할 수록 조건</strong><br>' + escape(scope)
                         + ' ' + link('관계의 근거', source) + '</p>')
        lines += ['</details>', '']
    return '\n'.join(lines)


def classical_formula_table(payload):
    """Follow explicit clause-to-formula and formula-to-herb records only."""
    nodes = {node['@id']: node for node in payload['@graph']}
    rows = defaultdict(set)
    herbs = defaultdict(set)
    for node in nodes.values():
        if node['@type'] != 'rdf:Statement':
            continue
        predicate = node['rdf:predicate']['@id']
        subject, target = node['rdf:subject']['@id'], node['rdf:object']['@id']
        if predicate == 'km:recordsFormula':
            if ('km:ClassicalPassage' not in nodes[subject]['@type']
                    or 'km:Formula' not in nodes[target]['@type']):
                raise ValueError('Invalid classical formula view types')
            rows[(subject, target, node['dcterms:source']['@id'])].add(node['skos:scopeNote']['@value'])
        elif predicate == 'km:containsHerb':
            herbs[subject].add(target)

    def label(key):
        return nodes[key]['skos:prefLabel']['@value']

    lines = ['| 원전 조문 | 수록된 처방 | 등록된 구성 본초·보조재료 | 조문의 조건·순서 |', '|---|---|---|---|']
    for clause, formula, source in sorted(rows):
        ingredients = ' · '.join(link(label(key), nodes[key]['foaf:page']['@id'])
                                 for key in sorted(herbs[formula], key=lambda key: (label(key), key)))
        contexts = ''.join('<p>' + escape(scope).replace('|', '&#124;').replace('\n', '<br>') + '</p>'
                           for scope in sorted(rows[(clause, formula, source)]))
        note = '<details class="ontology-clause-context"><summary>조건·순서 보기</summary>' + contexts + '</details>'
        lines.append('| ' + link(label(clause), source)
                     + ' | ' + link(label(formula), nodes[formula]['foaf:page']['@id'])
                     + ' | ' + ingredients + ' | ' + note + ' |')
    return '\n'.join(lines) + '\n'


def meridian_members(payload):
    """Browse only qualified belongsToMeridian records in the shared ontology."""
    nodes = {node['@id']: node for node in payload['@graph']}
    groups = defaultdict(set)
    sources = defaultdict(set)
    for node in nodes.values():
        if (node['@type'] != 'rdf:Statement'
                or node['rdf:predicate']['@id'] != 'km:belongsToMeridian'):
            continue
        point, meridian = node['rdf:subject']['@id'], node['rdf:object']['@id']
        if 'km:Acupoint' not in nodes[point]['@type'] or 'km:Meridian' not in nodes[meridian]['@type']:
            raise ValueError('Invalid meridian membership view types')
        groups[meridian].add(point)
        sources[meridian].add(node['dcterms:source']['@id'])

    def label(key):
        return nodes[key]['skos:prefLabel']['@value']

    def point_order(key):
        notation = nodes[key]['skos:notation']
        return (notation.rstrip('0123456789'), int(notation.lstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ')))

    lines = ['| 소속 경맥 | 경혈 수 | 전체 소속 경혈 | 소속표 출처 |', '|---|---:|---|---|']
    for meridian in sorted(groups, key=lambda key: (label(key), key)):
        points = ' · '.join(link(label(key), nodes[key]['foaf:page']['@id'])
                            for key in sorted(groups[meridian], key=point_order))
        refs = ' · '.join(link('소속 경혈표', url) for url in sorted(sources[meridian]))
        lines.append('| ' + link(label(meridian), nodes[meridian]['foaf:page']['@id'])
                     + ' | ' + str(len(groups[meridian])) + ' | ' + points + ' | ' + refs + ' |')
    return '\n'.join(lines) + '\n'


@lru_cache(maxsize=1)
def herb_payload(docs_dir):
    payload, _ = build_ontology(Path(docs_dir), ROOT / 'data/ontology.json')
    return payload


@lru_cache(maxsize=1)
def render_for_docs(docs_dir):
    payload, _ = build_ontology(Path(docs_dir), ROOT / 'data/ontology.json')
    return composition_tables(payload)


def on_pre_build(config, **kwargs):
    render_for_docs.cache_clear()
    herb_payload.cache_clear()


def on_page_markdown(markdown, *, page, config, files):
    if page.file.src_uri != 'network/index.md':
        if HERB_MARKER not in markdown:
            return markdown
        if not page.file.src_uri.startswith('herbs/') or markdown.count(HERB_MARKER) != 1:
            raise ValueError('Herb composition views require one marker in a herb document')
        rendered = herb_formula_table(herb_payload(str(config['docs_dir'])), page.file.src_uri)
        return markdown.replace(HERB_MARKER, rendered)
    if markdown.count(MARKER) != 1:
        raise ValueError('The network page needs exactly one ontology composition marker')
    markdown = markdown.replace(MARKER, render_for_docs(str(config['docs_dir'])))
    if VARIANT_MARKER in markdown:
        if markdown.count(VARIANT_MARKER) != 1:
            raise ValueError('The network page needs one formula variant marker')
        markdown = markdown.replace(VARIANT_MARKER, variant_comparisons(herb_payload(str(config['docs_dir']))))
    if CLASSICAL_MARKER in markdown:
        if markdown.count(CLASSICAL_MARKER) != 1:
            raise ValueError('The network page needs one classical formula marker')
        markdown = markdown.replace(CLASSICAL_MARKER, classical_formula_table(herb_payload(str(config['docs_dir']))))
    if MERIDIAN_MARKER in markdown:
        if markdown.count(MERIDIAN_MARKER) != 1:
            raise ValueError('The network page needs one meridian membership marker')
        markdown = markdown.replace(MERIDIAN_MARKER, meridian_members(herb_payload(str(config['docs_dir']))))
    return markdown
