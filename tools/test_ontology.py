"""Source integrity, formulation separation and qualified-assertion contracts."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from ontology import build_ontology, source_url, RESOURCE


class OntologyTests(unittest.TestCase):
    def setUp(self):
        self.docs = Path('docs')
        self.source = Path('data/ontology.json')
        self.data = json.loads(self.source.read_text(encoding='utf-8'))

    def build_modified(self, data):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'ontology.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            return build_ontology(self.docs, source)

    def test_same_name_formulas_keep_distinct_ids_and_sources(self):
        payload, stats = build_ontology(self.docs, self.source)
        variants = [node for node in payload['@graph']
                    if node.get('@id') in (RESOURCE + '#suanzaoren-jinkui',
                                           RESOURCE + '#suanzaoren-donguibogam')]
        self.assertEqual(len(variants), 2)
        self.assertNotEqual(variants[0]['foaf:page'], variants[1]['foaf:page'])
        self.assertEqual(variants[0]['skos:altLabel'], variants[1]['skos:altLabel'])
        self.assertNotIn('owl:sameAs', json.dumps(payload))
        self.assertGreater(stats['statement_count'], 0)
        self.assertEqual((payload, stats), build_ontology(self.docs, self.source))

    def test_all_assertions_retain_source_and_scope(self):
        payload, _ = build_ontology(self.docs, self.source)
        statements = [node for node in payload['@graph'] if node['@type'] == 'rdf:Statement']
        self.assertEqual(len(statements), len(self.data['statements']))
        for node in statements:
            for field in ('rdf:subject', 'rdf:predicate', 'rdf:object', 'dcterms:source'):
                self.assertTrue(node[field]['@id'].startswith('https:') or node[field]['@id'].startswith('km:'))
            self.assertTrue(node['skos:scopeNote']['@value'])
        # The qualification-bearing statement must not also become an
        # unqualified assertion that a client can consume without the scope.
        predicate_keys = {'km:' + key for key in self.data['predicates']}
        for node in payload['@graph']:
            self.assertFalse(predicate_keys.intersection(node))

    def test_missing_sources_and_fragments_fail_closed(self):
        for reference in ('formulas/missing.md', 'formulas/sijunzi-tang.md#absent',
                          '../AGENTS.md', '/tmp/file.md', 'https://example.org/source.md',
                          'formulas/sijunzi-tang.md?version=other'):
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                source_url(reference, self.docs)

    def test_invalid_semantic_records_fail_build(self):
        mutations = [
            lambda data: data['concepts'].append(deepcopy(data['concepts'][0])),
            lambda data: data['statements'].append(deepcopy(data['statements'][0])),
            lambda data: data['statements'][0].update(object='missing-concept'),
            lambda data: data['statements'][0].update(object='st36'),
            lambda data: data['statements'][0].update(predicate='cures'),
            lambda data: data['statements'][0].update(scope=''),
            lambda data: data['statements'][0].update(source='formulas/sijunzi-tang.md#absent'),
        ]
        for mutate in mutations:
            data = deepcopy(self.data)
            mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                self.build_modified(data)

    def test_formulation_conditions_survive_export(self):
        payload, _ = build_ontology(self.docs, self.source)
        statements = [node for node in payload['@graph'] if node['@type'] == 'rdf:Statement']
        liujunzi = [node for node in statements if node['rdf:subject']['@id'].endswith('#liujunzi-yixuexinwu')
                    and node['rdf:predicate']['@id'] == 'km:containsHerb']
        self.assertEqual(len(liujunzi), 8)
        self.assertTrue(all('반하 탕포칠차' in node['skos:scopeNote']['@value'] for node in liujunzi))
        jinkui = [node for node in statements if node['rdf:subject']['@id'].endswith('#suanzaoren-jinkui')
                  and node['rdf:predicate']['@id'] == 'km:containsHerb']
        self.assertEqual(len(jinkui), 5)
        self.assertFalse(any(node['rdf:object']['@id'].endswith('#fresh-ginger') for node in jinkui))


if __name__ == '__main__':
    unittest.main()
