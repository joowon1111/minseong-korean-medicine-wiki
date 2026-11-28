"""Sleep/digestion questions retain source-specific formula and treatment contexts."""
import json
from html import unescape
from pathlib import Path
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections, source_excerpt
from ontology_views import pattern_treatment_routes


class SleepOntologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/ontology.json').read_text())
        cls.concepts = {c['id']: c for c in cls.data['concepts']}
        cls.records = cls.data['statements']
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.pages = page_projections(cls.payload)

    def relation(self, subject, predicate):
        return [s for s in self.records if s['subject'] == subject and s['predicate'] == predicate]

    def test_sleep_and_digestion_question_returns_two_distinct_treatment_routes(self):
        expected = {
            'guibi-jisheng': ('heart-spleen-deficiency', 'tonify-qi-nourish-blood-calm-spirit'),
            'guibi-donguibogam': ('heart-spleen-deficiency', 'tonify-qi-nourish-blood-calm-spirit'),
            'wendan-sanyin': ('gallbladder-stomach-disharmony',
                              'regulate-qi-transform-phlegm-harmonize-stomach'),
        }
        for formula, (pattern, principle) in expected.items():
            with self.subTest(formula=formula):
                contexts = self.relation(formula, 'hasTraditionalPatternContext')
                self.assertEqual([r['object'] for r in contexts], [pattern])
                treatments = self.relation(pattern, 'hasTraditionalTreatmentPrinciple')
                self.assertEqual([r['object'] for r in treatments], [principle])
                self.assertIn('후대', contexts[0]['quote'])
                for record in contexts + treatments:
                    self.assertEqual(source_excerpt(record['source'], record['quote'], Path('docs')),
                                     record['quote'])
                    self.assertTrue(record['scope'])
        for pattern, alias in [('heart-spleen-deficiency', '心脾兩虛'),
                               ('gallbladder-stomach-disharmony', '膽胃不和')]:
            self.assertEqual(self.concepts[pattern]['type'], 'Pattern')
            self.assertEqual(self.concepts[pattern]['aliases'], [alias])
            self.assertNotIn('불면', self.concepts[pattern]['aliases'])

    def test_guibi_variants_and_wendan_base_keep_their_own_ingredients(self):
        members = lambda f: {s['object'] for s in self.relation(f, 'containsHerb')}
        early, later, wendan = map(members, ['guibi-jisheng', 'guibi-donguibogam', 'wendan-sanyin'])
        self.assertEqual(len(early), 8)
        self.assertEqual(len(later), 12)
        self.assertEqual(later - early, {'angelica', 'polygala', 'fresh-ginger', 'jujube-fruit'})
        self.assertIn('poria-spirit', early & later)
        self.assertEqual(wendan, {'pinellia', 'citrus-peel', 'poria', 'citrus-immature',
                                  'bamboo-shavings', 'licorice', 'fresh-ginger', 'jujube-fruit'})
        self.assertNotIn('coptis', wendan)
        condition = self.relation('wendan-sanyin', 'hasTraditionalPatternContext')[0]
        for text in ['권9 허번', '기본 6미', '생강·대조', '四大錢', '후대', '황련온담탕']:
            self.assertIn(text, condition['scope'])

    def test_both_endpoints_keep_each_source_and_scope_in_page_exports(self):
        relevant = {'guibi-jisheng', 'guibi-donguibogam', 'wendan-sanyin',
                    'heart-spleen-deficiency', 'gallbladder-stomach-disharmony'}
        for record in self.records:
            if record['subject'] not in relevant or record['predicate'] not in (
                    'hasTraditionalPatternContext', 'hasTraditionalTreatmentPrinciple'):
                continue
            for endpoint in ('subject', 'object'):
                path = self.concepts[record[endpoint]]['page'].split('#')[0]
                url = BASE + '/' + path[:-3] + '/'
                exported = next(n for n in self.pages[url]['payload']['@graph']
                                if n['@id'] == RESOURCE + '#statement-' + record['id'])
                self.assertEqual(exported['dcterms:description']['@value'], record['quote'])
                self.assertEqual(exported['skos:scopeNote']['@value'], record['scope'])

    def test_public_comparison_retains_both_qualified_sources(self):
        rendered = pattern_treatment_routes(self.payload)
        for fid in ['guibi-jisheng', 'guibi-donguibogam', 'wendan-sanyin']:
            context = self.relation(fid, 'hasTraditionalPatternContext')[0]
            treatment = self.relation(context['object'], 'hasTraditionalTreatmentPrinciple')[0]
            row = next(r for r in rendered.splitlines()
                       if r.startswith('| <a') and self.concepts[fid]['label'] in r)
            for record in [context, treatment]:
                path, anchor = record['source'].split('#')
                self.assertIn(BASE + '/' + path[:-3] + '/#' + anchor, row)
                self.assertIn(record['quote'], unescape(row))
        self.assertIn('>보기양혈·안신</a>', rendered)
        self.assertIn('>이기화담·화위이담</a>', rendered)


if __name__ == '__main__':
    unittest.main()
