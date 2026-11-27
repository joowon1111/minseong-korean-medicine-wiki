"""Render source-qualified composition relations in the existing network page."""
from collections import defaultdict
from functools import lru_cache
from html import escape
from pathlib import Path

from ontology import BASE, build_ontology

MARKER = '<!-- MINSEONG_ONTOLOGY_COMPOSITION_TABLES -->'
HERB_MARKER = '<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->'
MERIDIAN_MARKER = '<!-- MINSEONG_ONTOLOGY_MERIDIAN_MEMBERS -->'
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
    lines += ['', '각 수록형의 원문 약량·포제와 달일 때 더하는 재료는 출처 본문에서 함께 확인합니다. 산조인탕의 두 수록형은 각각의 이름과 출처를 유지하며, 복령·적복령·계심의 표기도 구분합니다.', '',
              '### 공통 본초에서 처방 찾아가기 {#ontology-shared-herbs}', '',
              '현재 두 개 이상의 처방 수록형에 구성 관계가 등록된 본초입니다. 인삼·복령·감초처럼 같은 본초가 여러 처방에 포함되는 경우 전체 배합과 출처를 비교할 수 있습니다.', '',
              '| 본초 | 구성 관계가 등록된 처방 수록형 |', '|---|---|']
    inverse = defaultdict(set)
    for formula, herbs in formulas.items():
        for herb in herbs:
            inverse[herb].add(formula)
    for herb in sorted(inverse, key=lambda key: (label(key), key)):
        if len(inverse[herb]) < 2:
            continue
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
    rows = set()
    for node in payload['@graph']:
        if (node['@type'] == 'rdf:Statement'
                and node['rdf:predicate']['@id'] == 'km:containsHerb'
                and node['rdf:object']['@id'] in herbs):
            rows.add((node['rdf:object']['@id'], node['rdf:subject']['@id'],
                      node['dcterms:source']['@id']))
    if not rows:
        raise ValueError('No explicit ontology composition records for ' + source_path)
    def label(key):
        return nodes[key]['skos:prefLabel']['@value']
    lines = ['| 원문 약명 | 처방 수록형 | 구성 출처 |', '|---|---|---|']
    for herb, formula, source in sorted(rows, key=lambda row: (label(row[0]), label(row[1]), row)):
        lines.append('| ' + link(label(herb), nodes[herb]['foaf:page']['@id'])
                     + ' | ' + link(label(formula), nodes[formula]['foaf:page']['@id'])
                     + ' | ' + link('원문·구성 확인', source) + ' |')
    lines += ['', '현재 온톨로지에 구성 관계가 등록된 수록형입니다. 원문 약량·포제와 달일 때 더하는 재료는 구성 출처에서 함께 확인합니다. '
              + link('전체 수록형의 구성 비교', BASE + '/network/#ontology-formula-compositions') + '에서도 이어 볼 수 있습니다.', '']
    return '\n'.join(lines)


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
    if MERIDIAN_MARKER in markdown:
        if markdown.count(MERIDIAN_MARKER) != 1:
            raise ValueError('The network page needs one meridian membership marker')
        markdown = markdown.replace(MERIDIAN_MARKER, meridian_members(herb_payload(str(config['docs_dir']))))
    return markdown
