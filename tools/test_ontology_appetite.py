"""Weak appetite queries retain source-specific ingredients and treatment routes."""
import test_ontology_food as food
from html import unescape
from pathlib import Path
from ontology import BASE, RESOURCE, source_excerpt
from ontology_views import herb_formula_table, pattern_treatment_routes
import unittest


class AppetiteFormulaQuestions(unittest.TestCase):
    setUpClass = classmethod(food.FoodFormulaQuestions.setUpClass.__func__)
    records = food.FoodFormulaQuestions.records

    def test_samchul_has_twelve_ingredients_and_two_decoction_adjuncts(self):
        records = {r['object']: r for r in self.records('samchul-geonbi-donguibogam')}
        self.assertEqual(set(records), {'ginseng','atractylodes','white-poria',
            'magnolia-bark','citrus-peel','hawthorn','citrus-immature','white-peony',
            'massa-medicata-fermentata','barley-malt','amomum','licorice',
            'fresh-ginger','jujube-fruit'})
        for herb in ['ginseng','hawthorn']:
            self.assertIn('一錢',records[herb]['quote'])
        for herb in ['citrus-immature','white-peony']:
            self.assertIn('八分',records[herb]['quote'])
        self.assertIn('3쪽',records['fresh-ginger']['quote'])
        self.assertIn('2매',records['jujube-fruit']['quote'])

    def test_preparation_conditions_are_not_transferred_between_formulas(self):
        for herb in ['massa-medicata-fermentata','barley-malt']:
            samchul=next(r for r in self.records('samchul-geonbi-donguibogam') if r['object']==herb)
            zheng=next(r for r in self.records('jiawei-erchen-yixuezhengzhuan') if r['object']==herb)
            self.assertIn('별도 포제·조입 표기 없음',samchul['quote'])
            self.assertIn('細研炒另包',zheng['scope'])
            self.assertNotIn('細研炒另包',samchul['scope'])
            self.assertIn('지실을 뺀 2002년',samchul['scope'])

    def test_herb_lookup_and_both_exports_keep_exact_quotes_and_scope(self):
        for r in self.records('samchul-geonbi-donguibogam'):
            with self.subTest(record=r['id']):
                self.assertEqual(source_excerpt(r['source'],r['quote'],Path('docs')),r['quote'])
                for endpoint in ['subject','object']:
                    path=self.concepts[r[endpoint]]['page'].split('#')[0]
                    graph=self.pages[BASE+'/'+path[:-3]+'/']['payload']['@graph']
                    node=next(n for n in graph if n['@id']==RESOURCE+'#statement-'+r['id'])
                    self.assertEqual(node['dcterms:description']['@value'],r['quote'])
                    self.assertEqual(node['skos:scopeNote']['@value'],r['scope'])
                herb=self.concepts[r['object']]['page'].split('#')[0]
                self.assertIn('<!-- MINSEONG_ONTOLOGY_HERB_FORMULAS -->',(Path('docs')/herb).read_text())
                rendered=unescape(herb_formula_table(self.payload,herb))
                self.assertIn(self.concepts['samchul-geonbi-donguibogam']['label'],rendered)
                self.assertIn(r['source'].split('#')[1],rendered)
                self.assertIn(r['scope'],rendered)

    def test_xiangsha_reuses_existing_phlegm_treatment_and_keeps_ten_memberships(self):
        self.assertEqual(len(self.records('xiangsha-liujunzi-shifang')),10)
        context=self.records('xiangsha-liujunzi-shifang','hasTraditionalPatternContext')
        self.assertEqual([r['object'] for r in context],['spleen-qi-deficiency-with-phlegm'])
        for text in ['木香·砂仁 각 八分','以行氣消脹','방약합편 12미형','소음인 동명방','현대 시험제제']:
            self.assertIn(text,context[0]['scope'])
        treatment=self.records(context[0]['object'],'hasTraditionalTreatmentPrinciple')
        self.assertEqual([r['object'] for r in treatment],['tonify-spleen-transform-phlegm'])

    def test_food_phlegm_and_weak_appetite_routes_preserve_qualified_sources(self):
        rendered=unescape(pattern_treatment_routes(self.payload))
        for fid,pattern,principle in [
            ('samchul-geonbi-donguibogam','spleen-stomach-qi-deficiency-with-food-stagnation','tonify-spleen-digest-food-harmonize-middle'),
            ('xiangsha-liujunzi-shifang','spleen-qi-deficiency-with-phlegm','tonify-spleen-transform-phlegm'),
            ('baohe-danxi','food-stagnation','digest-food-harmonize-stomach'),
            ('jiawei-erchen-yixuezhengzhuan','food-phlegm-stagnation','guide-phlegm-support-spleen-digest-food-regulate-qi')]:
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
