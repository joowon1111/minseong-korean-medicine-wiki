"""Source integrity, formulation separation and qualified-assertion contracts."""
from copy import deepcopy
import json
import re
from collections import Counter
from pathlib import Path
import tempfile
import unittest

from ontology import build_ontology, source_url, source_excerpt, RESOURCE


class OntologyTests(unittest.TestCase):
    def test_standard_memberships_cover_the_atlas_exactly_once(self):
        from test_meridian_routes import COUNTS
        catalog = json.loads(Path('data/acupoint_catalog.json').read_text())['points']
        manifest = json.loads(Path('data/standard_manifest.json').read_text())
        atlas = Path('docs/acupoint-network/standard-atlas.md').read_text()
        atlas_rows = re.findall(r'\[([^\]]+)\]\(\.\./(acupuncture/points/[^)]+\.md)\)', atlas)
        atlas_points = {re.search(r'([A-Z]{2}\d+)$', name)[1]: (name, path)
                        for name, path in atlas_rows}
        concepts = {c['id']: c for c in self.data['concepts']}
        points = [c for c in concepts.values() if c['type'] == 'Acupoint']
        self.assertEqual(len(points), 361)
        self.assertEqual(len({c['notation'] for c in points}), 361)
        self.assertEqual({c['notation'] for c in points}, set(catalog))
        self.assertEqual(set(atlas_points), set(catalog))
        self.assertEqual({p['code'] for p in manifest}, set(catalog))
        for identity in manifest:
            p = catalog[identity['code']]
            self.assertEqual(identity, {key: p[key] for key in identity})
        members = [s for s in self.data['statements'] if s['predicate'] == 'belongsToMeridian']
        self.assertEqual(Counter(s['subject'] for s in members), Counter(c['id'] for c in points))
        routes = json.loads(Path('data/meridian_routes.json').read_text())['routes']
        route_map = {Path(r['path']).stem: r for r in routes}
        self.assertEqual(Counter(concepts[s['subject']]['notation'].rstrip('0123456789')
                                 for s in members), COUNTS)
        self.assertEqual({s['object'] for s in members}, set(route_map))
        for s in members:
            c = concepts[s['subject']]
            p = catalog[c['notation']]
            route = route_map[s['object']]
            with self.subTest(code=p['code']):
                self.assertEqual(c['label'], p['name_ko'] + ' ' + p['code'])
                self.assertIn(p['name_zh'], c['aliases'])
                self.assertEqual(c['page'], p['path'])
                self.assertEqual(p['meridian_code'], route['code'])
                self.assertEqual(concepts[s['object']]['label'], p['meridian'])
                self.assertEqual(s['source'], route['path'] + '#_3')
                row = re.fullmatch(r'\| ([A-Z]+\d+) \| \[([^]]+)\]\(../([^)]*)\) \|', s['quote'])
                self.assertIsNotNone(row)
                self.assertEqual((row[1], row[3]), (p['code'], c['page']))
                self.assertEqual(source_excerpt(s['source'], s['quote'], self.docs), s['quote'])
                display = re.sub(r'\([^)]*\)', '', row[2]).removesuffix(' ' + p['code'])
                self.assertIn(display, [p['name_ko']] + c['aliases'])
                atlas_name, atlas_path = atlas_points[p['code']]
                self.assertEqual(atlas_path, c['page'])
                self.assertIn('(' + p['name_zh'] + ')', atlas_name)
                self.assertIn(atlas_name.split('(')[0], [p['name_ko']] + c['aliases'])
        # Exact code ranges catch missing and out-of-range points and extra points.
        self.assertEqual(set(catalog), {prefix + str(i) for prefix, count in COUNTS.items()
                                       for i in range(1, count + 1)})

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

    def test_pc6_and_st40_codes_and_meridian_membership_stay_distinct(self):
        payload, _ = build_ontology(self.docs, self.source)
        graph = {n['@id']: n for n in payload['@graph']}
        for point, notation, meridian, path in [
                ('pc6', 'PC6', 'pericardium-meridian', 'pericardium-meridian'),
                ('st40', 'ST40', 'stomach-meridian', 'stomach-meridian')]:
            concept = graph[RESOURCE + '#' + point]
            self.assertIn('km:Acupoint', concept['@type'])
            self.assertEqual(concept['skos:notation'], notation)
            statement = graph[RESOURCE + '#statement-' + point + '--belongsToMeridian--' + meridian]
            self.assertEqual(statement['rdf:subject']['@id'], concept['@id'])
            self.assertEqual(statement['rdf:object']['@id'], RESOURCE + '#' + meridian)
            self.assertEqual(statement['rdf:predicate']['@id'], 'km:belongsToMeridian')
            self.assertTrue(statement['dcterms:source']['@id'].endswith('/' + path + '/#_3'))
            self.assertIn(notation, statement['dcterms:description']['@value'])
            self.assertIn('분류 관계', statement['skos:scopeNote']['@value'])

    def test_navigation_graph_classifies_individual_meridians(self):
        from build_ai_knowledge_layer import entity_type, DOCS
        self.assertEqual(entity_type(DOCS / 'meridian-network/heart-meridian.md'), 'meridian')
        self.assertEqual(entity_type(DOCS / 'meridian-network/stomach-meridian.md'), 'meridian')
        for name in ('index.md', 'extraordinary-vessels.md', 'special-points/index.md'):
            self.assertNotEqual(entity_type(DOCS / 'meridian-network' / name), 'meridian')

    def test_banxia_houpo_preserves_five_ingredients_and_historical_units(self):
        payload, _ = build_ontology(self.docs, self.source)
        graph = {node['@id']: node for node in payload['@graph']}
        records = [node for node in graph.values() if node['@type'] == 'rdf:Statement'
                   and node['rdf:subject']['@id'] == RESOURCE + '#banxia-houpo-jinkui'
                   and node['rdf:predicate']['@id'] == 'km:containsHerb']
        self.assertEqual({node['rdf:object']['@id'].split('#')[-1] for node in records},
                         {'pinellia', 'magnolia-bark', 'poria', 'fresh-ginger', 'perilla-leaf'})
        for record in records:
            self.assertIn('반하 1승은 부피', record['skos:scopeNote']['@value'])
            self.assertIn('건소엽', record['skos:scopeNote']['@value'])
            self.assertTrue(record['dcterms:source']['@id'].endswith('/banxia-houpo-tang/#source-dose-original'))
        leaf = graph[RESOURCE + '#perilla-leaf']
        self.assertIn('乾蘇葉', leaf['skos:altLabel'])
        clause = graph[RESOURCE + '#statement-jinkui-22-005--recordsFormula--banxia-houpo-jinkui']
        self.assertEqual(clause['rdf:object']['@id'], RESOURCE + '#banxia-houpo-jinkui')
        self.assertTrue(clause['dcterms:source']['@id'].endswith('#clause-22-005'))

    def test_banxia_houpo_pattern_context_keeps_formulation_and_scope(self):
        payload, _ = build_ontology(self.docs, self.source)
        graph = {node['@id']: node for node in payload['@graph']}
        pattern = graph[RESOURCE + '#phlegm-qi-binding']
        self.assertEqual(pattern['@type'], ['skos:Concept', 'km:Pattern'])
        self.assertTrue(pattern['foaf:page']['@id'].endswith('/diagnostics/patterns/phlegm-fluid/#phlegm-qi-binding'))
        context = graph[RESOURCE + '#statement-banxia-houpo-jinkui--hasTraditionalPatternContext--phlegm-qi-binding']
        self.assertEqual(context['rdf:subject']['@id'], RESOURCE + '#banxia-houpo-jinkui')
        self.assertEqual(context['rdf:object']['@id'], pattern['@id'])
        self.assertEqual(context['rdf:predicate']['@id'], 'km:hasTraditionalPatternContext')
        self.assertIn('금궤요략 5미', context['skos:scopeNote']['@value'])
        self.assertIn('후대 변증', context['skos:scopeNote']['@value'])
        self.assertIn('실제 연하곤란', context['skos:scopeNote']['@value'])
        self.assertIn('담기울결의 맥락', context['dcterms:description']['@value'])

    def test_pattern_principle_route_preserves_qualified_edges(self):
        payload, _ = build_ontology(self.docs, self.source)
        nodes = {n['@id']: n for n in payload['@graph']}
        statements = [n for n in nodes.values() if n['@type'] == 'rdf:Statement']
        formula = RESOURCE + '#liujunzi-yixuexinwu'
        contexts = [n for n in statements if n['rdf:subject']['@id'] == formula
                    and n['rdf:predicate']['@id'] == 'km:hasTraditionalPatternContext']
        self.assertEqual({n['rdf:object']['@id'].split('#')[-1] for n in contexts},
                         {'qi-deficiency', 'spleen-qi-deficiency-with-phlegm'})
        for context in contexts:
            routes = [n for n in statements
                      if n['rdf:subject'] == context['rdf:object']
                      and n['rdf:predicate']['@id'] == 'km:hasTraditionalTreatmentPrinciple']
            self.assertEqual(len(routes), 1)
            target = nodes[routes[0]['rdf:object']['@id']]
            self.assertIn('km:TreatmentPrinciple', target['@type'])
            self.assertTrue(routes[0]['dcterms:description']['@value'])
            self.assertTrue(context['skos:scopeNote']['@value'])
        # A formula or herb cannot silently become the subject/target of a
        # Pattern -> TreatmentPrinciple relationship.
        for field, value in [('subject', 'liujunzi-yixuexinwu'), ('object', 'ginseng')]:
            data = deepcopy(self.data)
            relation = next(n for n in data['statements']
                            if n['predicate'] == 'hasTraditionalTreatmentPrinciple')
            relation[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build_modified(data)

    def test_navigation_distinguishes_patterns_from_treatment_guides(self):
        from build_ai_knowledge_layer import entity_type, relation_name, DOCS
        self.assertEqual(entity_type(DOCS / 'diagnostics/patterns/phlegm-fluid.md'), 'pattern')
        kind = entity_type(DOCS / 'pattern-treatment/phlegm-fluid.md')
        self.assertEqual(kind, 'treatment_principle_guide')
        self.assertEqual(relation_name(kind), 'links_to_treatment_principle')

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
