"""Six-stagnation questions preserve source identity, basic herbs and adjuncts."""
import json
from html import unescape
from pathlib import Path
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections, source_excerpt
from ontology_views import herb_formula_table, pattern_treatment_routes, variant_comparisons


class StagnationQuestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def records(self, fid, predicate='containsHerb'):
        return [s for s in self.data['statements'] if s['subject'] == fid and s['predicate'] == predicate]

    def members(self, fid):
        return {r['object'] for r in self.records(fid)}

    def test_does_liuyu_contain_both_banxia_and_shenqu_depends_on_source(self):
        early = self.members('liuyu-yixuerumen')
        later = self.members('liuyu-donguibogam-uigam')
        self.assertEqual(len(early), 10)  # nine basic herbs + boiling ginger
        self.assertEqual(len(later), 13)  # twelve basic herbs + boiling ginger
        self.assertEqual(early - later, {'pinellia', 'amomum'})
        self.assertEqual(later - early, {'massa-medicata-fermentata', 'forsythia',
                                      'beimu-source-name', 'citrus-aurantium-immature', 'perilla-leaf'})
        text = unescape(variant_comparisons(self.payload))
        panel = next(p for p in text.split('<details class="ontology-variant-comparison">')
                     if '육울탕 — 의학입문 9미 수록형' in p)
        self.assertIn('육울탕 — 동의보감 의감 인용 12미 수록형', panel)
        self.assertIn('생강 三片', panel)
        self.assertIn('신곡', panel)
        self.assertIn('반하', panel)

    def test_yueju_five_equal_parts_do_not_absorb_conditional_additions(self):
        self.assertEqual(self.members('yueju-yifang'), {'cyperus', 'chuanxiong',
                         'atractylodes-lancea', 'gardenia', 'massa-medicata-fermentata'})
        for record in self.records('yueju-yifang'):
            self.assertIn('등분', record['quote'])
            self.assertIn('曲糊為丸', record['scope'])
            self.assertIn('水丸', record['scope'])
            self.assertIn('조건부 가미', record['scope'])
        gardenia = next(r for r in self.records('yueju-yifang') if r['object'] == 'gardenia')
        self.assertIn('검게 볶음', gardenia['quote'])

    def test_same_korean_name_does_not_import_qinpi_or_imply_a_beimu_species(self):
        fid = 'liuyu-donguibogam-uigam'
        chenpi = next(r for r in self.records(fid) if r['object'] == 'citrus-peel')
        self.assertIn('陳皮', chenpi['quote'])
        self.assertNotIn('秦皮', chenpi['quote'])
        self.assertIn('동의보감', chenpi['scope'])
        beimu = next(r for r in self.records(fid) if r['object'] == 'beimu-source-name')
        self.assertIn('기원종은 이 대목에 미기재', beimu['quote'])
        self.assertEqual(self.concepts['beimu-source-name']['aliases'], ['貝母'])
        self.assertNotIn('천패모', self.concepts['beimu-source-name']['label'])

    def test_every_new_ingredient_keeps_quote_scope_and_both_public_page_exports(self):
        for fid in ['yueju-yifang', 'liuyu-yixuerumen', 'liuyu-donguibogam-uigam']:
            for record in self.records(fid):
                with self.subTest(record=record['id']):
                    source_excerpt(record['source'], record['quote'], Path('docs'))
                    herb = self.concepts[record['object']]['page'].split('#')[0]
                    text = unescape(herb_formula_table(self.payload, herb))
                    self.assertIn(record['scope'], text)
                    self.assertIn(self.concepts[fid]['label'], text)
                    self.assertIn('<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->', (Path('docs') / herb).read_text())
                    for endpoint in ['subject', 'object']:
                        path = self.concepts[record[endpoint]]['page'].split('#')[0]
                        node = next(n for n in self.pages[BASE + '/' + path[:-3] + '/']['payload']['@graph']
                                    if n['@id'] == RESOURCE + '#statement-' + record['id'])
                        self.assertEqual(node['dcterms:description']['@value'], record['quote'])
                        self.assertEqual(node['skos:scopeNote']['@value'], record['scope'])

    def test_three_source_formulations_keep_their_qualified_six_stagnation_route(self):
        text = unescape(pattern_treatment_routes(self.payload))
        treatment = self.records('six-stagnations', 'hasTraditionalTreatmentPrinciple')
        self.assertEqual([r['object'] for r in treatment], ['move-qi-release-stagnation'])
        for fid in ['yueju-yifang', 'liuyu-yixuerumen', 'liuyu-donguibogam-uigam']:
            contexts = self.records(fid, 'hasTraditionalPatternContext')
            self.assertEqual([r['object'] for r in contexts], ['six-stagnations'])
            row = next(l for l in text.splitlines() if self.concepts[fid]['label'] in l)
            for record in contexts + treatment:
                self.assertIn(record['quote'], row)
                self.assertIn(record['scope'], row)
                self.assertIn(record['source'].split('#')[1], row)


if __name__ == '__main__':
    unittest.main()
