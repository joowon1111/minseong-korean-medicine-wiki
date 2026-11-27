"""Source integrity, formulation separation and qualified-assertion contracts."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from ontology import build_ontology, source_url, source_excerpt, RESOURCE


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

    def test_exported_excerpts_match_the_source_statements(self):
        payload, _ = build_ontology(self.docs, self.source)
        original = {item['id']: item for item in self.data['statements']}
        statements = [node for node in payload['@graph'] if node['@type'] == 'rdf:Statement']
        for node in statements:
            key = node['@id'].split('#statement-', 1)[1]
            self.assertEqual(node['dcterms:description']['@value'], original[key]['quote'])
            source_excerpt(original[key]['source'], original[key]['quote'], self.docs)

    def test_empty_changed_or_non_text_excerpts_fail_build(self):
        for quote in ('', None, [], 'This excerpt no longer appears in the article.'):
            data = deepcopy(self.data)
            data['statements'][0]['quote'] = quote
            with self.subTest(quote=quote), self.assertRaises(ValueError):
                self.build_modified(data)

    def test_excerpt_must_be_in_the_cited_section(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory)
            page = docs / 'topic.md'
            page.write_text('## First {#first}\nOne.\n## Second {#second}\nEvidence.\n')
            with self.assertRaises(ValueError):
                source_excerpt('topic.md#first', 'Evidence.', docs)
            self.assertEqual(source_excerpt('topic.md#second', 'Evidence.', docs), 'Evidence.')
            page.write_text('## First {#first}\n### Detail\nEvidence.\n')
            self.assertEqual(source_excerpt('topic.md#first', 'Evidence.', docs), 'Evidence.')

    def test_hidden_anchors_and_excerpts_cannot_validate_a_source(self):
        hidden = [
            '<!-- ## Hidden {#fake}\nEvidence. -->',
            '<script>## Hidden {#fake}\nEvidence.</script>',
            '<style>## Hidden {#fake}\nEvidence.</style>',
            '<template>## Hidden {#fake}\nEvidence.</template>',
            '```markdown\n## Hidden {#fake}\nEvidence.\n```',
            '~~~markdown\n## Hidden {#fake}\nEvidence.\n~~~',
            '   ```markdown\n## Hidden {#fake}\nEvidence.\n   ```',
            '```markdown\n## Hidden {#fake}\nEvidence.',
            '    ## Hidden {#fake} Evidence.',
            '`## Hidden {#fake} Evidence.`',
            '---\ntitle: "Hidden {#fake} Evidence."\n---',
        ]
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory)
            for block in hidden:
                (docs / 'topic.md').write_text(block + '\n# Visible\nPlain text.\n')
                with self.subTest(block=block):
                    with self.assertRaises(ValueError):
                        source_url('topic.md#fake', docs)
                    with self.assertRaises(ValueError):
                        source_excerpt('topic.md', 'Evidence.', docs)

    def test_source_symlink_cannot_escape_public_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory) / 'docs'
            docs.mkdir()
            outside = Path(directory) / 'outside.md'
            outside.write_text('Private source')
            (docs / 'linked.md').symlink_to(outside)
            with self.assertRaises(ValueError):
                source_url('linked.md', docs)

    def test_shenmen_has_a_distinct_heart_meridian_relationship(self):
        payload, _ = build_ontology(self.docs, self.source)
        node = next(n for n in payload['@graph']
                    if n['@id'].endswith('#statement-ht7--belongsToMeridian--heart-meridian'))
        self.assertTrue(node['rdf:subject']['@id'].endswith('#ht7'))
        self.assertTrue(node['rdf:object']['@id'].endswith('#heart-meridian'))
        self.assertIn('신문 HT7', node['dcterms:description']['@value'])

    def test_navigation_graph_classifies_individual_meridians(self):
        from build_ai_knowledge_layer import entity_type, DOCS
        self.assertEqual(entity_type(DOCS / 'meridian-network/heart-meridian.md'), 'meridian')
        self.assertEqual(entity_type(DOCS / 'meridian-network/stomach-meridian.md'), 'meridian')
        for name in ('index.md', 'extraordinary-vessels.md', 'special-points/index.md'):
            self.assertNotEqual(entity_type(DOCS / 'meridian-network' / name), 'meridian')

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
        donguibogam = [node for node in statements
                       if node['rdf:subject']['@id'].endswith('#suanzaoren-donguibogam')
                       and node['rdf:predicate']['@id'] == 'km:containsHerb']
        ingredients = {node['rdf:object']['@id'].rsplit('#', 1)[1] for node in donguibogam}
        self.assertEqual(ingredients, {
            'gypsum', 'ziziphus-seed', 'ginseng', 'anemarrhena',
            'red-poria', 'licorice', 'cinnamon-heart', 'fresh-ginger',
        })
        jinkui_ingredients = {node['rdf:object']['@id'].rsplit('#', 1)[1] for node in jinkui}
        self.assertEqual(ingredients & jinkui_ingredients,
                         {'ziziphus-seed', 'anemarrhena', 'licorice'})
        ginger = next(node for node in donguibogam
                      if node['rdf:object']['@id'].endswith('#fresh-ginger'))
        self.assertIn('생강 3편', ginger['skos:scopeNote']['@value'])
        self.assertTrue(all(node['dcterms:source']['@id'].endswith('#donguibogam-version')
                            for node in donguibogam))


if __name__ == '__main__':
    unittest.main()
