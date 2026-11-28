"""Food/phlegm questions keep formulation, quantity and preparation records."""
import json
from html import unescape
from pathlib import Path
import unittest
from ontology import BASE, RESOURCE, build_ontology, page_projections, source_excerpt
from ontology_views import herb_formula_table, pattern_treatment_routes


class FoodFormulaQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def records(self, subject, predicate='containsHerb'):
        return [r for r in self.data['statements'] if r['subject']==subject and r['predicate']==predicate]

    def test_baohe_is_seven_ingredients_and_preserves_manufacturing_proportions(self):
        records = {r['object']:r for r in self.records('baohe-danxi')}
        self.assertEqual(set(records), {'hawthorn','massa-medicata-fermentata','pinellia',
                                       'poria','citrus-peel','forsythia','raphanus-seed'})
        for herb, quantity in [('hawthorn','6량'),('massa-medicata-fermentata','2량'),
                               ('pinellia','3량'),('poria','3량'),('raphanus-seed','1량')]:
            self.assertIn(quantity, records[herb]['quote'])
        for record in records.values():
            self.assertIn('炊餅',record['scope'])
            self.assertIn('每服七八十丸',record['scope'])
            self.assertIn('전체 제조 배합',record['scope'])
            self.assertIn('백출·황금',record['scope'])

    def test_zhengzhuan_keeps_twelve_herbs_two_adjuncts_and_exact_part_names(self):
        records = {r['object']:r for r in self.records('jiawei-erchen-yixuezhengzhuan')}
        self.assertEqual(set(records), {'citrus-red-peel','poria','pinellia','licorice',
            'chuanxiong','atractylodes-lancea','atractylodes','hawthorn','amomum',
            'massa-medicata-fermentata','cyperus','barley-malt','fresh-ginger','jujube-fruit'})
        self.assertIn('橘紅',records['citrus-red-peel']['quote'])
        self.assertIn('茯苓',records['poria']['quote'])
        self.assertIn('山楂肉',records['hawthorn']['quote'])
        self.assertIn('一枚',records['jujube-fruit']['quote'])
        self.assertIn('三片',records['fresh-ginger']['quote'])
        self.assertIn('湯泡洗',records['pinellia']['quote'])
        self.assertIn('炙',records['licorice']['quote'])
        self.assertIn('三分',records['licorice']['quote'])

    def test_shenqu_and_malt_question_returns_separate_packaging_and_late_mixing(self):
        for herb in ['massa-medicata-fermentata','barley-malt']:
            r=next(r for r in self.records('jiawei-erchen-yixuezhengzhuan') if r['object']==herb)
            self.assertIn('另包',r['scope'])
            self.assertIn('별포',r['quote'])
            self.assertIn('조입',r['quote'])
            self.assertIn('細研炒另包',r['scope'])
            self.assertIn('水二盞煎至一盞',r['scope'])
            rendered=unescape(herb_formula_table(self.payload,self.concepts[herb]['page'].split('#')[0]))
            self.assertIn(r['scope'],rendered)
            self.assertIn('정전가미이진탕 — 의학정전 도담보비 수록형',rendered)

    def test_both_formula_and_herb_exports_keep_all_qualified_composition_records(self):
        for fid in ['baohe-danxi','jiawei-erchen-yixuezhengzhuan']:
            for r in self.records(fid):
                with self.subTest(record=r['id']):
                    self.assertEqual(source_excerpt(r['source'],r['quote'],Path('docs')),r['quote'])
                    for endpoint in ['subject','object']:
                        path=self.concepts[r[endpoint]]['page'].split('#')[0]
                        page=self.pages[BASE+'/'+path[:-3]+'/']['payload']['@graph']
                        node=next(n for n in page if n['@id']==RESOURCE+'#statement-'+r['id'])
                        self.assertEqual(node['dcterms:description']['@value'],r['quote'])
                        self.assertEqual(node['skos:scopeNote']['@value'],r['scope'])
                    herb=self.concepts[r['object']]['page'].split('#')[0]
                    self.assertIn('<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->',(Path('docs')/herb).read_text())

    def test_food_phlegm_and_weakness_questions_have_three_distinct_treatment_routes(self):
        expected={
            'baohe-danxi':('food-stagnation','digest-food-harmonize-stomach'),
            'jiawei-erchen-yixuezhengzhuan':('food-phlegm-stagnation','guide-phlegm-support-spleen-digest-food-regulate-qi'),
            'liujunzi-yixuexinwu':('spleen-qi-deficiency-with-phlegm','tonify-spleen-transform-phlegm'),
        }
        rendered=unescape(pattern_treatment_routes(self.payload))
        for fid,(pattern,principle) in expected.items():
            context=next(r for r in self.records(fid,'hasTraditionalPatternContext') if r['object']==pattern)
            treatment=self.records(pattern,'hasTraditionalTreatmentPrinciple')
            self.assertEqual([r['object'] for r in treatment],[principle])
            row=next(l for l in rendered.splitlines() if self.concepts[fid]['label'] in l and self.concepts[pattern]['label'] in l)
            for r in [context]+treatment:
                self.assertIn(r['quote'],row)
                self.assertIn(r['scope'],row)
                self.assertIn(r['source'].split('#')[1],row)


if __name__=='__main__':
    unittest.main()
