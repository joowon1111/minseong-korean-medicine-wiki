"""Export source-qualified editorial concepts as SKOS and RDF statements.

Document links remain in the navigation graph. Only explicitly curated records
become ontology concepts; assertions retain their source and scope as RDF
reification, rather than losing their qualifications in bare semantic triples.
"""
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

BASE = 'https://wiki.minseong.co.kr'
RESOURCE = BASE + '/assets/ai/ontology.jsonld'
TYPES = {
    'Formula': '처방 수록형', 'Herb': '본초', 'Pattern': '한의학 변증',
    'Acupoint': '경혈', 'Meridian': '경맥', 'ClassicalPassage': '고전 조문',
}
IDENTIFIER = re.compile(r'^[a-z][a-z0-9-]*$')


def visible_source(file: Path) -> str:
    """Return source prose without metadata, hidden markup or code examples."""
    text = file.read_text(encoding='utf-8-sig')
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) == 3:
            text = parts[2]
    text = re.sub(r'<!--.*?(?:-->|\Z)', '', text, flags=re.S)
    text = re.sub(r'<(script|style|template)\b[^>]*>.*?(?:</\1\s*>|\Z)',
                  '', text, flags=re.I | re.S)
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^[ ]{0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.fullmatch(r'[ ]{0,3}' + re.escape(fence[0])
                            + '{' + str(len(fence)) + r',}[ \t]*', line.rstrip('\r\n')):
                fence = None
            continue
        if marker:
            fence = marker.group(1)
            continue
        if line.startswith(('    ', '\t')):
            continue
        lines.append(line)
    return re.sub(r'(`+).*?\1', '', ''.join(lines))


def source_url(reference: str, docs: Path) -> str:
    """Require a real public Markdown source and, when used, an explicit anchor."""
    parts = urlsplit(reference)
    path = Path(parts.path)
    if (parts.scheme or parts.netloc or parts.query or path.is_absolute()
            or '..' in path.parts or path.suffix != '.md'):
        raise ValueError(f'Invalid ontology source: {reference}')
    file = docs / path
    if not file.is_file():
        raise ValueError(f'Missing ontology source: {reference}')
    try:
        file.resolve().relative_to(docs.resolve())
    except ValueError:
        raise ValueError(f'Ontology source escapes public docs: {reference}')
    if parts.fragment:
        text = visible_source(file)
        anchors = set(re.findall(r'\{#([^}\s]+)\}', text))
        anchors.update(re.findall(r'''\bid=["']([^"']+)["']''', text))
        if parts.fragment not in anchors:
            raise ValueError(f'Missing explicit ontology anchor: {reference}')
    relative = path.as_posix()[:-3]
    if relative == 'index':
        relative = ''
    elif relative.endswith('/index'):
        relative = relative[:-6]
    url = BASE + '/' + (relative + '/' if relative else '')
    return url + ('#' + parts.fragment if parts.fragment else '')


def source_excerpt(reference: str, quote: str, docs: Path) -> str:
    """Require an exact excerpt in the cited visible heading section."""
    source_url(reference, docs)
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError(f'Missing ontology excerpt: {reference}')
    parts = urlsplit(reference)
    passage = visible_source(docs / parts.path)
    if parts.fragment:
        heading = re.search(
            r'^(#{1,6})[ \t]+[^\n]*\{#' + re.escape(parts.fragment)
            + r'\}[^\n]*(?:\n|$)', passage, flags=re.M)
        if heading is None:
            raise ValueError(f'Ontology excerpt needs an explicit Markdown heading: {reference}')
        passage = passage[heading.end():]
        boundary = re.search(r'^#{1,' + str(len(heading.group(1))) + r'}[ \t]+',
                             passage, flags=re.M)
        if boundary:
            passage = passage[:boundary.start()]
    if quote not in passage:
        raise ValueError(f'Stale/misplaced ontology excerpt: {reference}')
    return quote


def build_ontology(docs: Path, source: Path) -> tuple[dict, dict]:
    data = json.loads(source.read_text(encoding='utf-8'))
    if data['version'] != '1.0':
        raise ValueError('Unsupported ontology source version')
    concepts = {}
    for item in data['concepts']:
        key = item['id']
        if not IDENTIFIER.fullmatch(key) or key in concepts:
            raise ValueError(f'Invalid/duplicate ontology concept: {key}')
        if item['type'] not in TYPES:
            raise ValueError(f'Unknown ontology type: {item["type"]}')
        if not item['label'].strip() or not item['definition'].strip():
            raise ValueError(f'Missing ontology label/definition: {key}')
        source_url(item['page'], docs)
        concepts[key] = item
    predicates = data['predicates']
    for key, item in predicates.items():
        if not re.fullmatch(r'[a-z][a-zA-Z]+', key):
            raise ValueError(f'Invalid ontology predicate: {key}')
        if item['domain'] not in TYPES or item['range'] not in TYPES:
            raise ValueError(f'Unknown domain/range: {key}')
        if not item['label'].strip() or not item['definition'].strip():
            raise ValueError(f'Missing ontology predicate definition: {key}')
    seen = set()
    triples = set()
    for item in data['statements']:
        if not IDENTIFIER.fullmatch(item['id'].lower()) or item['id'] in seen:
            raise ValueError(f'Invalid/duplicate ontology statement: {item["id"]}')
        seen.add(item['id'])
        if item['subject'] not in concepts or item['object'] not in concepts:
            raise ValueError(f'Dangling ontology statement: {item["id"]}')
        if item['predicate'] not in predicates:
            raise ValueError(f'Unknown ontology predicate: {item["predicate"]}')
        predicate = predicates[item['predicate']]
        if (concepts[item['subject']]['type'] != predicate['domain']
                or concepts[item['object']]['type'] != predicate['range']):
            raise ValueError(f'Ontology domain/range mismatch: {item["id"]}')
        key = (item['subject'], item['predicate'], item['object'], item['source'], item['scope'])
        if key in triples or item['subject'] == item['object']:
            raise ValueError(f'Duplicate/self ontology statement: {item["id"]}')
        triples.add(key)
        if not item['scope'].strip():
            raise ValueError(f'Missing ontology scope: {item["id"]}')
        source_excerpt(item['source'], item.get('quote'), docs)

    namespace = RESOURCE + '#'
    scheme = namespace + 'scheme'
    graph = [{
        '@id': scheme, '@type': 'skos:ConceptScheme',
        'dcterms:title': {'@value': '민성 한의학 온톨로지 — 출처 기반 개념·관계', '@language': 'ko'},
        'dcterms:hasVersion': data['version'],
        'rdfs:seeAlso': {'@id': BASE + '/network/#ontology-data'},
        'skos:scopeNote': {'@value': '기존 본문에서 선별한 개념과 관계. rdf:Statement의 subject·predicate·object는 source와 scopeNote를 함께 읽는다. 문서 탐색 링크는 별도 knowledge-graph.json에 제공한다.', '@language': 'ko'},
    }]
    for key, label in sorted(TYPES.items()):
        graph.append({'@id': 'km:' + key, '@type': 'rdfs:Class',
                      'rdfs:label': {'@value': label, '@language': 'ko'},
                      'rdfs:subClassOf': {'@id': 'skos:Concept'}})
    for key, item in sorted(predicates.items()):
        graph.append({'@id': 'km:' + key, '@type': 'rdf:Property',
                      'rdfs:label': {'@value': item['label'], '@language': 'ko'},
                      'rdfs:comment': {'@value': item['definition'], '@language': 'ko'},
                      'rdfs:domain': {'@id': 'km:' + item['domain']},
                      'rdfs:range': {'@id': 'km:' + item['range']}})
    for key, item in sorted(concepts.items()):
        node = {'@id': namespace + key, '@type': ['skos:Concept', 'km:' + item['type']],
                'skos:inScheme': {'@id': scheme},
                'skos:prefLabel': {'@value': item['label'], '@language': 'ko'},
                'skos:altLabel': item.get('aliases', []),
                'skos:definition': {'@value': item['definition'], '@language': 'ko'},
                'foaf:page': {'@id': source_url(item['page'], docs)}}
        if item.get('notation'):
            node['skos:notation'] = item['notation']
        graph.append(node)
    for item in sorted(data['statements'], key=lambda row: row['id']):
        graph.append({'@id': namespace + 'statement-' + item['id'], '@type': 'rdf:Statement',
                      'rdf:subject': {'@id': namespace + item['subject']},
                      'rdf:predicate': {'@id': 'km:' + item['predicate']},
                      'rdf:object': {'@id': namespace + item['object']},
                      'dcterms:source': {'@id': source_url(item['source'], docs)},
                      'dcterms:description': {'@value': item['quote']},
                      'skos:scopeNote': {'@value': item['scope'], '@language': 'ko'}})
    return {'@context': {
        'km': namespace, 'skos': 'http://www.w3.org/2004/02/skos/core#',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'dcterms': 'http://purl.org/dc/terms/', 'foaf': 'http://xmlns.com/foaf/0.1/',
    }, '@graph': graph}, {
        'concept_count': len(concepts), 'statement_count': len(seen),
        'predicate_count': len(predicates), 'source_version': data['version'],
    }


def page_projections(payload: dict) -> dict[str, dict]:
    """Project only curated concepts, incident statements and source-page context.

    Keep global IDs and all qualifications. Neighbor concepts are included to
    resolve statement endpoints; concept_ids identifies only this page's own
    concepts. Ordinary document links and shared labels never create membership.
    """
    from collections import defaultdict

    def page_url(url):
        return url.split('#', 1)[0]

    nodes = {node['@id']: node for node in payload['@graph']}
    concepts = {key: node for key, node in nodes.items()
                if isinstance(node.get('@type'), list) and 'skos:Concept' in node['@type']}
    own = defaultdict(set)
    statements = defaultdict(set)
    for key, node in concepts.items():
        own[page_url(node['foaf:page']['@id'])].add(key)
    for key, node in nodes.items():
        if node.get('@type') != 'rdf:Statement':
            continue
        subject, target = node['rdf:subject']['@id'], node['rdf:object']['@id']
        pages = {page_url(concepts[subject]['foaf:page']['@id']),
                 page_url(concepts[target]['foaf:page']['@id']),
                 page_url(node['dcterms:source']['@id'])}
        for url in pages:
            statements[url].add(key)
    vocabulary = {key for key, node in nodes.items()
                  if node.get('@type') in ('rdfs:Class', 'rdf:Property', 'skos:ConceptScheme')}
    result = {}
    for url in sorted(own.keys() | statements.keys()):
        selected = set(own[url]) | statements[url] | vocabulary
        for key in statements[url]:
            selected.update((nodes[key]['rdf:subject']['@id'], nodes[key]['rdf:object']['@id']))
        result[url] = {
            'concept_ids': sorted(own[url]),
            'statement_ids': sorted(statements[url]),
            'payload': {'@context': payload['@context'],
                        '@graph': [nodes[key] for key in sorted(selected)]},
        }
    return result
