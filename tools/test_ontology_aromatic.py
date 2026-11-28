"""Aromatic formula questions preserve source parts and per-dose preparation."""
import unittest
import test_ontology_food as food
from pathlib import Path
from html import unescape
from ontology import BASE, RESOURCE, source_excerpt
from ontology_views import herb_formula_table, pattern_treatment_routes

class AromaticFormulaQuestions(unittest.TestCase):
    setUpClass = classmethod(food.FoodFormulaQuestions.setUpClass.__func__)
    records = food.FoodFormulaQuestions.records

    def test_xiangsha_pingwei_is_nine_herbs_and_ginger_without_jujube(self):
        records={r['object']:r for r in self.records('xiangsha-pingwei-donguibogam')}
        self.assertEqual(set(records),{'atractylodes-lancea','citrus-peel','cyperus','citrus-immature','agastache','magnolia-bark','amomum','aucklandia','licorice','fresh-ginger'})
        for h,q in [('atractylodes-lancea','二錢'),('cyperus','一錢'),('citrus-immature','八分'),('amomum','七分'),('licorice','五分'),('fresh-ginger','3쪽')]:
            self.assertIn(q,records[h]['quote'])

    def test_yangwei_keeps_ju_hong_poria_and_tsaoko_without_later_jujube(self):
        records={r['object']:r for r in self.records('renshen-yangwei-guofang')}
        self.assertEqual(set(records),{'pinellia','magnolia-bark','atractylodes-lancea','agastache','tsaoko-fruit','poria','ginseng','licorice','citrus-red-peel','fresh-ginger','mume-fruit'})
        for h,q in [('tsaoko-fruit','去皮·膜'),('citrus-red-peel','七錢半'),('pinellia','湯洗七次'),('fresh-ginger','七片'),('mume-fruit','一個')]:
            self.assertIn(q,records[h]['quote'])
        for r in records.values():
            for term in ['每服四錢','水一盞半','煎至六分','제조 총량','대조는 이 수록형에 없다']:
                self.assertIn(term,r['scope'])

    def test_formula_and_herb_exports_retain_exact_visible_source_and_scope(self):
        for fid in ['xiangsha-pingwei-donguibogam','renshen-yangwei-guofang']:
            for r in self.records(fid):
                with self.subTest(record=r['id']):
                    self.assertEqual(source_excerpt(r['source'],r['quote'],Path('docs')),r['quote'])
                    for endpoint in ['subject','object']:
                        path=self.concepts[r[endpoint]]['page'].split('#')[0]
                        graph=self.pages[BASE+'/'+path[:-3]+'/']['payload']['@graph']
                        n=next(n for n in graph if n['@id']==RESOURCE+'#statement-'+r['id'])
                        self.assertEqual(n['dcterms:description']['@value'],r['quote'])
                        self.assertEqual(n['skos:scopeNote']['@value'],r['scope'])

    def test_every_ingredient_has_a_visible_qualified_reverse_lookup(self):
        for fid in ['xiangsha-pingwei-donguibogam','renshen-yangwei-guofang']:
            for r in self.records(fid):
                herb=self.concepts[r['object']]['page'].split('#')[0]
                self.assertIn('<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->',(Path('docs')/herb).read_text())
                rendered=unescape(herb_formula_table(self.payload,herb))
                self.assertIn(self.concepts[fid]['label'],rendered)
                self.assertIn(r['scope'],rendered)

    def test_food_injury_and_external_cold_have_distinct_qualified_treatment_routes(self):
        rendered=unescape(pattern_treatment_routes(self.payload))
        for fid,pattern,principle in [
            ('xiangsha-pingwei-donguibogam','food-injury-qi-damp-stagnation','regulate-qi-transform-damp-harmonize-stomach'),
            ('renshen-yangwei-guofang','external-wind-cold-internal-raw-cold','warm-middle-release-exterior-transform-damp')]:
            context=self.records(fid,'hasTraditionalPatternContext')
            self.assertEqual([r['object'] for r in context],[pattern])
            treatment=self.records(pattern,'hasTraditionalTreatmentPrinciple')
            self.assertEqual([r['object'] for r in treatment],[principle])
            row=next(l for l in rendered.splitlines() if self.concepts[fid]['label'] in l and self.concepts[pattern]['label'] in l)
            for r in context+treatment:
                self.assertIn(r['quote'],row)
                self.assertIn(r['scope'],row)
                self.assertIn(r['source'].split('#')[1],row)

if __name__=='__main__':unittest.main()
