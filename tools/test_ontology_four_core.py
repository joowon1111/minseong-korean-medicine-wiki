"""Source-qualified answers to dizziness, sleep and digestive formula questions."""
import json
from html import escape, unescape
from pathlib import Path
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections, source_excerpt
from ontology_views import composition_tables, herb_formula_table, pattern_treatment_routes, variant_comparisons


class FourCoreFormulaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.statements = cls.data['statements']
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def records(self, formula, predicate='containsHerb'):
        return [s for s in self.statements if s['subject'] == formula and s['predicate'] == predicate]

    def members(self, formula):
        return {s['object'] for s in self.records(formula)}

    def test_baizhu_and_tianma_question_retains_white_poria_processing_and_dose(self):
        fid = 'banxia-baizhu-tianma-piwei'
        self.assertEqual(self.members(fid), {
            'phellodendron', 'dried-ginger', 'gastrodia', 'atractylodes-lancea',
            'white-poria', 'astragalus', 'alisma', 'ginseng', 'atractylodes',
            'massa-medicata-fermentata', 'pinellia', 'barley-malt', 'citrus-peel'})
        records = {r['object']: r for r in self.records(fid)}
        self.assertIn('5分', records['gastrodia']['quote'])
        self.assertIn('1전', records['atractylodes']['quote'])
        self.assertIn('주세', records['phellodendron']['quote'])
        self.assertIn('초(볶음)', records['massa-medicata-fermentata']['quote'])
        for r in records.values():
            self.assertIn('半兩', r['scope'])
            self.assertIn('식전', r['scope'])
            self.assertIn('별도 수록형', r['scope'])

    def test_tianwang_question_distinguishes_base_alternative_coating_and_modern_product(self):
        fid = 'tianwang-buxin-yifang'
        self.assertEqual(self.members(fid), {
            'fresh-rehmannia', 'ginseng', 'scrophularia', 'salvia', 'poria',
            'platycodon', 'polygala', 'ziziphus-seed', 'thuja-seed', 'asparagus-root',
            'ophiopogon', 'angelica', 'schisandra', 'honey'})
        poria = next(r for r in self.records(fid) if r['object'] == 'poria')
        self.assertIn('대용', poria['scope'])
        self.assertIn('역사적 환의', poria['scope'])
        self.assertIn('현대 주사 제외 제제', poria['scope'])
        self.assertIn('묶어 읽은 해석', poria['scope'])
        thuja = next(r for r in self.records(fid) if r['object'] == 'thuja-seed')
        self.assertIn('기름기 제거', thuja['quote'])

    def test_shugan_question_keeps_zhike_shaoyao_and_two_meanings_of_fen(self):
        fid = 'chaihu-shugan-jingyue'
        self.assertEqual(self.members(fid), {
            'citrus-peel', 'bupleurum', 'chuanxiong', 'citrus-aurantium-immature',
            'shaoyao-source-name', 'licorice', 'cyperus'})
        zhike = next(r for r in self.records(fid) if r['object'] == 'citrus-aurantium-immature')
        self.assertIn('밀기울로 볶음', zhike['quote'])
        self.assertIn('煎八分', zhike['scope'])
        self.assertIn('감초 炙 五分', zhike['scope'])
        self.assertIn('식초로 볶음', next(r for r in self.records(fid) if r['object'] == 'citrus-peel')['quote'])

    def test_jiawei_namesake_question_has_two_complete_different_formulations(self):
        early, domestic = map(self.members, ['jiawei-wendan-wanbing', 'jiawei-wendan-bangyak'])
        self.assertEqual(len(early), 13)  # 11 base herbs + two boiling adjuncts
        self.assertEqual(len(domestic), 13)
        self.assertEqual(early - domestic, {
            'citrus-peel', 'poria', 'ziziphus-seed', 'polygala', 'schisandra', 'prepared-rehmannia'})
        self.assertEqual(domestic - early, {
            'citrus-red-peel', 'white-poria', 'cyperus', 'platycodon', 'ophiopogon', 'bupleurum'})
        for r in self.records('jiawei-wendan-wanbing'):
            self.assertIn('各一錢，一分', r['scope'])
            self.assertIn('개수는 미기재', r['scope'])
        for r in self.records('jiawei-wendan-bangyak'):
            self.assertIn('생강 3편·대조 2매', r['scope'])
            self.assertIn('DB 환산', r['scope'])
        compared = unescape(variant_comparisons(self.payload))
        self.assertIn('가미온담탕 — 만병회춘 허번 수록형', compared)
        self.assertIn('가미온담탕 — 방약합편 향부자·맥문동 수록형', compared)
        self.assertIn('各一錢，一分', compared)
        self.assertIn('생강 3편·대조 2매', compared)

    def test_every_new_composition_survives_reverse_view_and_both_page_exports(self):
        fids = {'banxia-baizhu-tianma-piwei', 'tianwang-buxin-yifang',
                'chaihu-shugan-jingyue', 'jiawei-wendan-wanbing', 'jiawei-wendan-bangyak'}
        table = composition_tables(self.payload)
        for r in self.statements:
            if r['subject'] not in fids or r['predicate'] != 'containsHerb':
                continue
            with self.subTest(record=r['id']):
                self.assertEqual(source_excerpt(r['source'], r['quote'], Path('docs')), r['quote'])
                herb = self.concepts[r['object']]['page'].split('#')[0]
                rendered = herb_formula_table(self.payload, herb)
                label = self.concepts[r['subject']]['label']
                row = next(l for l in rendered.splitlines() if escape(label) in l)
                self.assertIn(r['scope'], unescape(row))
                self.assertIn(label, unescape(table))
                self.assertIn('<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->', (Path('docs') / herb).read_text())
                for endpoint in ['subject', 'object']:
                    path = self.concepts[r[endpoint]]['page'].split('#')[0]
                    url = BASE + '/' + path[:-3] + '/'
                    node = next(n for n in self.pages[url]['payload']['@graph']
                                if n['@id'] == RESOURCE + '#statement-' + r['id'])
                    self.assertEqual(node['skos:scopeNote']['@value'], r['scope'])
                    self.assertEqual(node['dcterms:description']['@value'], r['quote'])

    def test_clinical_questions_keep_four_distinct_qualified_treatment_routes(self):
        expected = {
            'banxia-baizhu-tianma-piwei': ('spleen-qi-deficiency-with-phlegm', 'tonify-spleen-transform-phlegm'),
            'tianwang-buxin-yifang': ('heart-kidney-yin-blood-deficiency', 'nourish-yin-blood-calm-heart'),
            'chaihu-shugan-jingyue': ('liver-qi-stagnation', 'soothe-liver-regulate-qi-move-blood-relieve-pain'),
            'jiawei-wendan-wanbing': ('heart-gallbladder-timidity', 'regulate-qi-transform-phlegm-calm-spirit'),
        }
        rendered = unescape(pattern_treatment_routes(self.payload))
        for fid, (pid, tid) in expected.items():
            self.assertEqual([r['object'] for r in self.records(fid, 'hasTraditionalPatternContext')], [pid])
            treatment = self.records(pid, 'hasTraditionalTreatmentPrinciple')
            self.assertEqual([r['object'] for r in treatment], [tid])
            row = next(l for l in rendered.splitlines() if self.concepts[fid]['label'] in l)
            for r in self.records(fid, 'hasTraditionalPatternContext') + treatment:
                self.assertIn(r['quote'], row)
                self.assertIn(r['scope'], row)
                self.assertIn(r['source'].split('#')[1], row)


if __name__ == '__main__':
    unittest.main()
