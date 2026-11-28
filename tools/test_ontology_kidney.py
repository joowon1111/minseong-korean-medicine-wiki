"""Kidney-pattern routes preserve formulation, ingredient identity and source conditions."""
import json
from pathlib import Path
import re
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections, source_excerpt
from ontology_views import herb_formula_table


class KidneyOntologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.records = cls.data['statements']
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def members(self, formula):
        return {s['object']: s for s in self.records
                if s['subject'] == formula and s['predicate'] == 'containsHerb'}

    def test_jingyue_formulas_have_exact_source_rows_and_distinct_ingredients(self):
        left = self.members('zuogui-jingyue')
        right = self.members('yougui-jingyue')
        self.assertEqual(len(left), 8)
        self.assertEqual(len(right), 10)
        common = {'prepared-rehmannia', 'dioscorea', 'cornus-fruit', 'wolfberry-fruit',
                  'cuscuta-seed', 'deer-antler-gelatin'}
        self.assertEqual(set(left) & set(right), common)
        self.assertEqual(set(left) - set(right), {'chuan-niuxi', 'turtle-plastron-gelatin'})
        self.assertEqual(set(right) - set(left), {'eucommia', 'angelica', 'cinnamon-bark', 'aconite'})
        for formula, members in [('zuogui-jingyue', left), ('yougui-jingyue', right)]:
            source = self.concepts[formula]['page']
            text = Path('docs', source.split('#')[0]).read_text()
            section = text.split('{#source-dose-original}', 1)[1].split('\n## ', 1)[0]
            visible_rows = {line for line in section.splitlines() if line.startswith('| [')}
            self.assertEqual({s['quote'] for s in members.values()}, visible_rows)
            for record in members.values():
                self.assertEqual(record['source'], source)
                self.assertEqual(source_excerpt(source, record['quote'], Path('docs')), record['quote'])
        self.assertNotIn('deer-antler', set(left) | set(right))
        self.assertNotIn('achyranthes', left)
        self.assertNotIn('turtle-plastron-gelatin', right)
        self.assertNotIn('fresh-ginger', right)  # 薑湯炒 is a processing instruction for 杜仲.

    def test_conditional_omissions_and_historical_adjustments_remain_visible(self):
        left, right = self.members('zuogui-jingyue'), self.members('yougui-jingyue')
        self.assertIn('精滑者，不用', left['chuan-niuxi']['scope'])
        self.assertIn('無火者，不必用', left['turtle-plastron-gelatin']['scope'])
        self.assertIn('敲碎·炒珠', left['deer-antler-gelatin']['scope'])
        self.assertIn('便溏勿用', right['angelica']['scope'])
        self.assertIn('二兩，漸可加至四兩', right['cinnamon-bark']['scope'])
        self.assertIn('自二兩，漸可加至五、六兩', right['aconite']['scope'])
        self.assertIn('현대 1일량으로 환산하지 않는다', right['aconite']['scope'])
        self.assertIn('생강탕으로 볶음', right['eucommia']['scope'])

    def test_chuan_niuxi_and_gelatins_keep_their_own_source_names(self):
        niuxi = self.concepts['chuan-niuxi']
        self.assertEqual(niuxi['aliases'], ['川牛膝'])
        self.assertEqual(niuxi['page'], 'herbs/achyranthes.md#processing')
        self.assertNotEqual(niuxi['id'], self.concepts['achyranthes']['id'])
        text = herb_formula_table(self.payload, 'herbs/achyranthes.md')
        self.assertIn('>천우슬</a>', text)
        self.assertIn('>우슬</a>', text)
        self.assertIn('좌귀환 — 경악전서 수록형', text)
        self.assertEqual(self.concepts['deer-antler-gelatin']['aliases'], ['鹿角膠', '鹿膠'])
        self.assertNotEqual(self.concepts['deer-antler-gelatin']['page'], self.concepts['deer-antler']['page'])

    def test_four_formula_pattern_principle_routes_keep_both_source_records(self):
        expected = {
            'liuwei-xiaoer': ('kidney-yin-deficiency', 'nourish-kidney-yin'),
            'zuogui-jingyue': ('kidney-yin-deficiency', 'nourish-kidney-yin'),
            'shenqi-jinkui': ('kidney-yang-deficiency', 'warm-kidney-yang'),
            'yougui-jingyue': ('kidney-yang-deficiency', 'warm-kidney-yang'),
        }
        for formula, (pattern, principle) in expected.items():
            with self.subTest(formula=formula):
                context = next(s for s in self.records if s['subject'] == formula
                               and s['predicate'] == 'hasTraditionalPatternContext')
                self.assertEqual(context['object'], pattern)
                treatment = next(s for s in self.records if s['subject'] == pattern
                                 and s['predicate'] == 'hasTraditionalTreatmentPrinciple')
                self.assertEqual(treatment['object'], principle)
                for record in (context, treatment):
                    for concept in (record['subject'], record['object']):
                        page = self.concepts[concept]['page'].split('#')[0]
                        subset = self.pages[BASE + '/' + page[:-3] + '/']['payload']['@graph']
                        projected = next(n for n in subset if n['@id'] == RESOURCE + '#statement-' + record['id'])
                        self.assertEqual(projected['dcterms:description']['@value'], record['quote'])
                        self.assertEqual(projected['skos:scopeNote']['@value'], record['scope'])
        pediatric = next(s for s in self.records if s['subject'] == 'liuwei-xiaoer'
                         and s['predicate'] == 'hasTraditionalPatternContext')
        self.assertIn('후대', pediatric['quote'])
        self.assertIn('소아 원문', pediatric['scope'])
        self.assertIn('신겁', pediatric['scope'])
        original = self.members('shenqi-jinkui')
        self.assertIn('dried-rehmannia', original)
        self.assertIn('cinnamon-twig', original)
        self.assertNotIn('prepared-rehmannia', original)
        self.assertNotIn('cinnamon-bark', original)

    def test_patterns_remain_traditional_concepts_and_old_anchors_are_preserved(self):
        for key, alias in [('kidney-yin-deficiency', '腎陰虛'), ('kidney-yang-deficiency', '腎陽虛')]:
            self.assertEqual(self.concepts[key]['type'], 'Pattern')
            self.assertEqual(self.concepts[key]['aliases'], [alias])
        for file, count in [('diagnostics/differentials/kidney-yin-vs-yang.md', 7),
                            ('diagnostics/patterns/kidney-deficiency.md', 5)]:
            text = Path('docs', file).read_text()
            for number in range(1, count + 1):
                self.assertEqual(len(re.findall(r'\{#_' + str(number) + r'\}', text)), 1)


if __name__ == '__main__':
    unittest.main()
