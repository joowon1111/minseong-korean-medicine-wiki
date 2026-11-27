"""Curated formula coverage, source variants and ingredient identity contracts."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

from ontology import build_ontology, page_projections, RESOURCE, BASE, visible_source
from ontology_views import composition_tables, herb_formula_table


class FormulaExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.members = [s for s in cls.data['statements'] if s['predicate'] == 'containsHerb']
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def herbs(self, fid):
        return {s['object'] for s in self.members if s['subject'] == fid}

    def records(self, fid):
        return [s for s in self.members if s['subject'] == fid]

    def test_main_formulas_have_their_expected_basic_and_explicit_adjunct_counts(self):
        expected = {
            'siwu-guofang': 4, 'bazhen-wanbing': 8, 'shiquan-guofang': 10,
            'buzhong-piwei': 8, 'danggui-buxue-neiwaishang': 2,
            'liuwei-xiaoer': 6, 'shenqi-jinkui': 8, 'guibi-jisheng': 8,
            'ssanghwa-guofang': 7, 'shengmai-yixuexinwu': 3,
            'gyeongok-hongshi': 4, 'erchen-guofang': 6, 'wendan-sanyin': 8,
            'pingwei-guofang': 4, 'xiangsha-liujunzi-shifang': 10,
            'banxia-xiexin-shanghan': 7, 'xiaochaihu-shanghan': 7,
            'guizhi-shanghan': 5, 'gegen-shanghan': 7,
            'xiaoqinglong-shanghan': 8, 'maimendong-jinkui': 6,
            'danggui-shaoyao-jinkui': 6, 'guizhi-fuling-jinkui': 5,
            'duhuo-jisheng-qianjin': 15, 'shujing-huoxue-wanbing': 16,
            'huanglian-jiedu-yifang': 4, 'wuling-shanghan': 5,
            'guibi-donguibogam': 12, 'shengmai-donguibogam': 3,
            'gyeongok-donguibogam-ipmun': 4, 'gyeongok-donguibogam-wisaeng': 4,
        }
        for fid, count in expected.items():
            with self.subTest(formula=fid):
                self.assertEqual(len(self.records(fid)), count)
                self.assertEqual(len(self.herbs(fid)), count)
                page, anchor = self.concepts[fid]['page'].split('#')
                text = visible_source(Path('docs') / page)
                heading = re.search(r'^(#{1,6})[^\n]*\{#' + re.escape(anchor) + r'\}[^\n]*\n', text, re.M)
                passage = text[heading.end():]
                end = re.search(r'^#{1,' + str(len(heading[1])) + r'} ', passage, re.M)
                if end:
                    passage = passage[:end.start()]
                table_rows = re.findall(r'^\| \[[^]]+\]\(../herbs/[^)]+\) · [^\n]+$', passage, re.M)
                quoted = {s['quote'] for s in self.records(fid)}
                self.assertTrue(set(table_rows).issubset(quoted))

    def test_every_formula_ingredient_has_one_membership_and_a_resolved_herb(self):
        pairs = [(s['subject'], s['object']) for s in self.members]
        self.assertEqual(len(pairs), len(set(pairs)))
        for s in self.members:
            self.assertEqual(self.concepts[s['subject']]['type'], 'Formula')
            self.assertEqual(self.concepts[s['object']]['type'], 'Herb')
            self.assertTrue(s['source'].startswith('formulas/'))
            self.assertIn('#', s['source'])
            self.assertTrue(s['scope'])

    def test_guibi_variants_preserve_danggui_yuanzhi_and_fushen(self):
        early, later = self.herbs('guibi-jisheng'), self.herbs('guibi-donguibogam')
        self.assertNotIn('angelica', early)
        self.assertNotIn('polygala', early)
        self.assertEqual(later - early, {'angelica', 'polygala', 'fresh-ginger', 'jujube-fruit'})
        self.assertIn('poria-spirit', early & later)
        self.assertNotIn('poria', early | later)

    def test_original_peony_and_white_peony_are_distinct(self):
        self.assertIn('white-peony', self.herbs('siwu-guofang'))
        for fid in ['guizhi-shanghan', 'guizhi-fuling-jinkui', 'danggui-shaoyao-jinkui']:
            self.assertIn('shaoyao-source-name', self.herbs(fid))
            self.assertNotIn('white-peony', self.herbs(fid))
        self.assertEqual(self.concepts['shaoyao-source-name']['aliases'], ['芍藥'])
        text = herb_formula_table(self.payload, 'herbs/white-peony.md')
        self.assertIn('>작약</a>', text)
        self.assertIn('>백작약</a>', text)

    def test_rehmannia_cinnamon_and_poria_identities_are_not_merged(self):
        original = self.herbs('shenqi-jinkui')
        self.assertTrue({'dried-rehmannia', 'cinnamon-twig', 'aconite'}.issubset(original))
        self.assertFalse({'prepared-rehmannia', 'cinnamon-bark'}.intersection(original))
        self.assertIn('prepared-rehmannia', self.herbs('liuwei-xiaoer'))
        self.assertIn('cinnamon-heart', self.herbs('duhuo-jisheng-qianjin'))
        self.assertNotIn('cinnamon-bark', self.herbs('duhuo-jisheng-qianjin'))
        self.assertNotIn('dipsacus', self.herbs('duhuo-jisheng-qianjin'))
        self.assertTrue({'citrus-red-peel', 'white-poria'}.issubset(self.herbs('erchen-guofang')))
        self.assertFalse({'citrus-peel', 'poria'}.intersection(self.herbs('erchen-guofang')))

    def test_preparation_adjuncts_and_historical_units_remain_qualified(self):
        for fid in ['erchen-guofang', 'wendan-sanyin', 'xiangsha-liujunzi-shifang']:
            for record in self.records(fid):
                if record['object'] == 'fresh-ginger':
                    self.assertIn('전탕', record['scope'])
        xiexin = self.herbs('banxia-xiexin-shanghan')
        self.assertIn('dried-ginger', xiexin)
        self.assertNotIn('fresh-ginger', xiexin)
        bq = next(s for s in self.records('buzhong-piwei') if s['object'] == 'astragalus')
        self.assertIn('五分', bq['scope'])
        original = next(s for s in self.records('shengmai-yixuexinwu') if s['object'] == 'schisandra')
        later = next(s for s in self.records('shengmai-donguibogam') if s['object'] == 'schisandra')
        self.assertIn('15립', original['quote'])
        self.assertIn('1전', later['quote'])
        self.assertNotEqual(original['source'], later['source'])

    def test_gyeongok_variants_preserve_three_manufacturing_ratios(self):
        ids = ['gyeongok-hongshi', 'gyeongok-donguibogam-ipmun', 'gyeongok-donguibogam-wisaeng']
        for fid in ids:
            self.assertEqual(self.herbs(fid), {'ginseng', 'fresh-rehmannia', 'white-poria', 'honey'})
        original = next(s for s in self.records(ids[0]) if s['object'] == 'white-poria')
        self.assertIn('49량', original['quote'])
        for fid, amount in zip(ids[1:], ['48량', '24량']):
            record = next(s for s in self.records(fid) if s['object'] == 'white-poria')
            self.assertIn(amount, record['scope'])
            self.assertIn('| 수록형 | 생지황 | 인삼 | 백복령 | 백밀 |', record['quote'])

    def test_registered_herbs_can_all_be_found_in_reverse_table(self):
        text = composition_tables(self.payload).split('### 본초에서 처방 찾아가기', 1)[1]
        herb_ids = {s['object'] for s in self.members}
        rows = [line for line in text.splitlines() if line.startswith('| <a')]
        self.assertEqual(len(rows), len(herb_ids))
        # One-formula herbs must remain discoverable, as well as common herbs.
        self.assertIn('>갱미</a>', text)
        self.assertIn('>승마</a>', text)
        self.assertIn('>황기</a>', text)

    def test_all_formula_and_herb_pages_preserve_bidirectional_source_records(self):
        for s in self.members:
            source = self.concepts[s['subject']]['page'].split('#')[0]
            herb = self.concepts[s['object']]['page'].split('#')[0]
            for path in [source, herb]:
                page = self.pages[BASE + '/' + path[:-3] + '/']
                self.assertIn(RESOURCE + '#statement-' + s['id'], page['statement_ids'])
                graph = {n['@id']: n for n in page['payload']['@graph']}
                record = graph[RESOURCE + '#statement-' + s['id']]
                self.assertEqual(record['dcterms:description']['@value'], s['quote'])
                self.assertEqual(record['skos:scopeNote']['@value'], s['scope'])


if __name__ == '__main__':
    unittest.main()
