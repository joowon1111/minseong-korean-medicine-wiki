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
    if parts.fragment:
        text = file.read_text(encoding='utf-8')
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
        source_url(item['source'], docs)

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
