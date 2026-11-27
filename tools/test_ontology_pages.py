"""Document subsets preserve identities, qualifications and source-only roles."""
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from ontology import build_ontology, page_projections, BASE, RESOURCE
import page_discovery as discovery
from audit_page_discovery import audit


class OntologyPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def test_incoming_compositions_keep_all_source_specific_variants(self):
        data = self.pages[BASE + '/herbs/ginseng/']
        self.assertIn(RESOURCE + '#ginseng', data['concept_ids'])
        graph = {node['@id']: node for node in data['payload']['@graph']}
        statements = [graph[key] for key in data['statement_ids']]
        self.assertTrue({RESOURCE + '#' + key for key in ('sijunzi-guofang', 'liujunzi-yixuexinwu', 'suanzaoren-donguibogam')}.issubset(
            {node['rdf:subject']['@id'] for node in statements if node['rdf:predicate']['@id'] == 'km:containsHerb'}))
        originals = {node['@id']: node for node in self.payload['@graph']}
        for node in statements:
            self.assertEqual(node, originals[node['@id']])
            self.assertIn('skos:scopeNote', node)
            self.assertIn('dcterms:description', node)
            self.assertIn(node['rdf:object']['@id'], graph)
            self.assertIn(node['rdf:subject']['@id'], graph)
            self.assertIn(node['rdf:predicate']['@id'], graph)

    def test_same_page_variants_stay_distinct_and_source_pages_have_no_own_concept(self):
        variants = self.pages[BASE + '/formulas/suanzaoren-tang/']
        self.assertTrue({RESOURCE + '#suanzaoren-jinkui', RESOURCE + '#suanzaoren-donguibogam'}.issubset(variants['concept_ids']))
        source = self.pages[BASE + '/compare/sijunzi-vs-liujunzi/']
        self.assertEqual(source['concept_ids'], [])
        self.assertTrue(any('sharesFormulaStructureWith' in key for key in source['statement_ids']))
        self.assertNotIn(BASE + '/conditions/insomnia/', self.pages)

    def test_banxia_houpo_clausal_and_ingredient_paths_keep_qualifications(self):
        formula = self.pages[BASE + '/formulas/banxia-houpo-tang/']
        self.assertEqual(formula['concept_ids'], [RESOURCE + '#banxia-houpo-jinkui'])
        self.assertEqual(len(formula['statement_ids']), 7)
        clause = self.pages[BASE + '/classics/jinkui-yaolue/chapters/gynecology/']
        self.assertEqual(clause['concept_ids'], [RESOURCE + '#jinkui-22-005'])
        self.assertEqual(len(clause['statement_ids']), 1)
        for slug in ('perilla-leaf', 'magnolia-bark'):
            herb = self.pages[BASE + '/herbs/' + slug + '/']
            self.assertEqual(herb['concept_ids'], [RESOURCE + '#' + slug])
            self.assertEqual(len(herb['statement_ids']), 1)
            record = next(n for n in herb['payload']['@graph'] if n['@type'] == 'rdf:Statement')
            self.assertEqual(record['rdf:subject']['@id'], RESOURCE + '#banxia-houpo-jinkui')
            self.assertIn('skos:scopeNote', record)
            self.assertIn('dcterms:description', record)

    def test_projection_is_deterministic_and_does_not_modify_global_payload(self):
        before = deepcopy(self.payload)
        self.assertEqual(page_projections(self.payload), self.pages)
        self.assertEqual(before, self.payload)
        point = self.pages[BASE + '/acupuncture/points/st36-zusanli/']
        self.assertEqual(point['concept_ids'], [RESOURCE + '#st36'])
        self.assertTrue(any('belongsToMeridian' in key for key in point['statement_ids']))

    def test_unrelated_docs_do_not_load_the_repository_ontology(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory) / 'docs'
            docs.mkdir()
            discovery.on_pre_build({'docs_dir': str(docs)})
            self.assertEqual(discovery._ontology_pages, {})

    def test_page_export_and_audit_detect_corrupted_subsets_and_missing_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            url = BASE + '/herbs/ginseng/'
            # A one-page fixture with one directly described concept keeps the
            # sitemap contract focused on document discovery rather than size.
            concept = deepcopy(next(n for n in self.payload['@graph'] if n['@id'] == RESOURCE + '#ginseng'))
            global_payload = {'@context': self.payload['@context'], '@graph': [concept]}
            pages = page_projections(global_payload)
            config = {'site_url': BASE + '/', 'site_name': 'Archive', 'site_dir': directory}
            page = SimpleNamespace(title='인삼', canonical_url=url, meta={},
                                   file=SimpleNamespace(src_uri='herbs/ginseng.md', dest_uri='herbs/ginseng/index.html'))
            files = SimpleNamespace(get_file_from_path=lambda path: None)
            discovery.on_pre_build(config)
            with patch.object(discovery, '_ontology_pages', pages):
                content = discovery.on_page_content('<h2 id="source">출처</h2><p>본문</p>', page, config, files)
                output = discovery.on_post_page('<head></head>' + content, page, config)
                discovery.on_post_build(config)
            document_path = site / 'assets/ai/pages/herbs/ginseng/index.json'
            document = json.loads(document_path.read_text())
            self.assertEqual(document['ontology']['concept_ids'], [RESOURCE + '#ginseng'])
            self.assertIn('rel="describedby" type="application/ld+json"', output)
            html_path = site / 'herbs/ginseng/index.html'
            html_path.parent.mkdir(parents=True)
            html_path.write_text(output)
            (site / 'assets/ai/ontology.jsonld').write_text(json.dumps(global_payload))
            (site / 'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + url + '</loc></url></urlset>')
            self.assertEqual(audit(site), (1, 1))
            subset_path = site / 'assets/ai/ontology-pages/herbs/ginseng/index.jsonld'
            original = subset_path.read_text()
            corrupt = json.loads(original)
            corrupt['@graph'][0]['skos:definition']['@value'] = '다른 설명'
            subset_path.write_text(json.dumps(corrupt))
            with self.assertRaisesRegex(ValueError, 'Ontology projection mismatch'):
                audit(site)
            subset_path.write_text(original)
            document.pop('ontology')
            document_path.write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, 'Ontology discovery metadata mismatch'):
                audit(site)
            discovery.on_pre_build(config)
            self.assertEqual(discovery._ontology_pages, {})


if __name__ == '__main__':
    unittest.main()
