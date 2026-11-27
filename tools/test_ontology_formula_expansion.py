"""Curated formula coverage, source variants and ingredient identity contracts."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

from ontology import build_ontology, page_projections, RESOURCE, BASE, visible_source
from ontology_views import composition_tables, herb_formula_table, classical_formula_table


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

    def test_added_core_formulas_preserve_basic_and_adjunct_counts(self):
        expected = {'yupingfeng-danxi': 3, 'shaoyao-gancao-shanghan': 2,
                    'huangqi-guizhi-wuwu-jinkui': 5, 'huangqi-jianzhong-jinkui': 7,
                    'lizhong-shanghan': 4, 'xiaoyao-guofang': 6,
                    'jiawei-xiaoyao-neike': 8, 'renshen-yangrong-guofang': 14,
                    'shenling-baizhu-guofang': 10, 'huoxiang-zhengqi-guofang': 11,
                    'xiaojianzhong-shanghan': 6, 'xiaojianzhong-jinkui': 6}
        for fid, count in expected.items():
            with self.subTest(formula=fid):
                self.assertEqual(len(self.records(fid)), count)
                self.assertEqual(len(self.herbs(fid)), count)

    def test_jianzhong_versions_preserve_source_specific_amounts(self):
        self.assertEqual(self.herbs('xiaojianzhong-shanghan'), self.herbs('xiaojianzhong-jinkui'))
        for fid, amount, dates in [('xiaojianzhong-shanghan', '2량', '20매'),
                                   ('xiaojianzhong-jinkui', '3량', '12매')]:
            records = {s['object']: s for s in self.records(fid)}
            self.assertIn('甘草 ' + amount, records['licorice']['scope'])
            self.assertIn('大棗 ' + dates, records['jujube-fruit']['scope'])
            self.assertIn('1승', records['maltose']['scope'])
        base = self.herbs('xiaojianzhong-jinkui')
        self.assertEqual(self.herbs('huangqi-jianzhong-jinkui') - base, {'astragalus'})
        self.assertFalse({'pinellia', 'poria'}.intersection(self.herbs('huangqi-jianzhong-jinkui')))
        # The five-herb base does not inherit ginseng from 一方有人參.
        five = self.herbs('huangqi-guizhi-wuwu-jinkui')
        self.assertNotIn('ginseng', five)
        self.assertNotIn('licorice', five)

    def test_processing_and_explicit_white_peony_remain_distinct(self):
        self.assertIn('pinellia-ferment', self.herbs('huoxiang-zhengqi-guofang'))
        self.assertNotIn('pinellia', self.herbs('huoxiang-zhengqi-guofang'))
        ferment = next(s for s in self.records('huoxiang-zhengqi-guofang')
                       if s['object'] == 'pinellia-ferment')
        self.assertIn('半夏曲', ferment['quote'])
        self.assertIn('발효', ferment['scope'])
        self.assertIn('white-peony', self.herbs('xiaoyao-guofang'))
        self.assertIn('shaoyao-source-name', self.herbs('jiawei-xiaoyao-neike'))
        white = next(s for s in self.records('xiaoyao-guofang') if s['object'] == 'white-peony')
        self.assertIn('芍藥（白）', white['quote'])
        self.assertNotIn('chuanxiong', self.herbs('renshen-yangrong-guofang'))
        for record in self.records('renshen-yangrong-guofang'):
            if record['object'] in {'fresh-ginger', 'jujube-fruit'}:
                self.assertIn('전탕 추가', record['scope'])

    def test_visible_clauses_name_the_exact_source_specific_formulas(self):
        expected = {
            'shanghan-012': {'guizhi-shanghan'},
            'shanghan-029': {'shaoyao-gancao-shanghan'},
            'shanghan-031': {'gegen-shanghan'},
            'shanghan-040': {'xiaoqinglong-shanghan'},
            'shanghan-096': {'xiaochaihu-shanghan'},
            'shanghan-100': {'xiaojianzhong-shanghan', 'xiaochaihu-shanghan'},
            'shanghan-149': {'banxia-xiexin-shanghan'},
            'jinkui-06-002': {'huangqi-guizhi-wuwu-jinkui'},
            'jinkui-06-013': {'xiaojianzhong-jinkui'},
            'jinkui-06-014': {'huangqi-jianzhong-jinkui'},
            'jinkui-06-015': {'shenqi-jinkui'},
            'jinkui-07-010': {'maimendong-jinkui'},
            'jinkui-20-005': {'danggui-shaoyao-jinkui'},
        }
        for cid, targets in expected.items():
            records = [s for s in self.data['statements'] if s['subject'] == cid
                       and s['predicate'] == 'recordsFormula']
            with self.subTest(clause=cid):
                self.assertEqual({s['object'] for s in records}, targets)
                self.assertEqual(self.concepts[cid]['type'], 'ClassicalPassage')
                for record in records:
                    self.assertTrue(record['quote'].startswith('> '))
                    self.assertEqual(record['source'], self.concepts[cid]['page'])
        records = {s['object']: s for s in self.data['statements']
                   if s['subject'] == 'shanghan-100'}
        self.assertIn('先與', records['xiaojianzhong-shanghan']['scope'])
        self.assertIn('不差者', records['xiaochaihu-shanghan']['scope'])

    def test_clause_and_formula_pages_share_the_same_qualified_record(self):
        for record in self.data['statements']:
            if record['predicate'] != 'recordsFormula':
                continue
            sid = RESOURCE + '#statement-' + record['id']
            for endpoint in ['subject', 'object']:
                path = self.concepts[record[endpoint]]['page'].split('#')[0]
                page = self.pages[BASE + '/' + path[:-3] + '/']
                self.assertIn(sid, page['statement_ids'])
                exported = next(n for n in page['payload']['@graph'] if n['@id'] == sid)
                self.assertEqual(exported['skos:scopeNote']['@value'], record['scope'])
                self.assertEqual(exported['dcterms:description']['@value'], record['quote'])

    def test_classical_table_only_follows_curated_relations(self):
        from copy import deepcopy
        text = classical_formula_table(self.payload)
        expected = {(s['subject'], s['object'], s['source']) for s in self.data['statements']
                    if s['predicate'] == 'recordsFormula'}
        self.assertEqual(len([line for line in text.splitlines() if line.startswith('| <a')]), len(expected))
        self.assertIn('#clause-100', text)
        self.assertIn('소건중탕 — 상한론 송본 수록형', text)
        self.assertIn('소건중탕 — 금궤요략 수록형', text)
        self.assertIn('/herbs/maltose/', text)
        payload = deepcopy(self.payload)
        record = deepcopy(next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                               and n['rdf:predicate']['@id'] == 'km:recordsFormula'))
        record['@id'] += '-navigation'
        record['rdf:predicate']['@id'] = 'km:links_to_formula'
        payload['@graph'].append(record)
        self.assertEqual(text, classical_formula_table(payload))

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
