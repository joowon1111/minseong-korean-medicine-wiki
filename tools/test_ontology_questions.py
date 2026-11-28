"""Practitioner questions must survive export and the public reverse lookup.

These are composition/source questions, not clinical efficacy assessments.
"""
from html import escape, unescape
from pathlib import Path
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections
from ontology_views import herb_formula_table, pattern_treatment_routes


class PractitionerQuestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))
        cls.nodes = {n['@id']: n for n in cls.payload['@graph']}
        cls.pages = page_projections(cls.payload)
        cls.records = [n for n in cls.nodes.values() if n['@type'] == 'rdf:Statement']

    def ingredient_records(self, herb):
        return [n for n in self.records
                if n['rdf:predicate']['@id'] == 'km:containsHerb'
                and n['rdf:object']['@id'] == RESOURCE + '#' + herb]

    def assert_public_answer(self, record, rendered):
        """A visible answer must retain the source and scope on both pages."""
        formula = self.nodes[record['rdf:subject']['@id']]
        row = next(line for line in rendered.splitlines()
                   if escape(formula['skos:prefLabel']['@value']) in line)
        self.assertIn(record['dcterms:source']['@id'], row)
        self.assertIn(escape(record['skos:scopeNote']['@value']), row)
        for endpoint in ('rdf:subject', 'rdf:object'):
            page = self.nodes[record[endpoint]['@id']]['foaf:page']['@id'].split('#')[0]
            projected = {n['@id']: n for n in self.pages[page]['payload']['@graph']}
            self.assertEqual(projected[record['@id']], record)

    def test_does_suanzaoren_tang_contain_ginseng_depends_on_source(self):
        # “산조인탕에 인삼이 들어가나요?” A shared formula name is insufficient.
        records = self.ingredient_records('ginseng')
        variants = {n['rdf:subject']['@id'].split('#')[-1]: n for n in records
                    if n['rdf:subject']['@id'].split('#')[-1]
                    in {'suanzaoren-jinkui', 'suanzaoren-donguibogam'}}
        self.assertEqual(set(variants), {'suanzaoren-donguibogam'})
        rendered = herb_formula_table(self.payload, 'herbs/ginseng.md')
        self.assert_public_answer(variants['suanzaoren-donguibogam'], rendered)
        self.assertIn('/suanzaoren-tang/#donguibogam-version', rendered)
        self.assertNotIn('/suanzaoren-tang/#source-dose-original', rendered)
        # Absence of an ontology edge alone is not proof of ingredient absence:
        # also check the cited, explicit five-ingredient base formulation.
        base = [n for n in self.records
                if n['rdf:predicate']['@id'] == 'km:containsHerb'
                and n['rdf:subject']['@id'] == RESOURCE + '#suanzaoren-jinkui']
        self.assertEqual({n['rdf:object']['@id'].split('#')[-1] for n in base},
                         {'ziziphus-seed', 'anemarrhena', 'poria', 'chuanxiong', 'licorice'})

    def test_which_sources_include_baizhu_in_sijunzi_and_liujunzi(self):
        # “백출이 들어간 사군자탕과 육군자탕의 출전·포제는?”
        rendered = herb_formula_table(self.payload, 'herbs/atractylodes.md')
        records = {n['rdf:subject']['@id'].split('#')[-1]: n
                   for n in self.ingredient_records('atractylodes')}
        for fid, source, condition in [
                ('sijunzi-guofang', 'sijunzi-tang', '태평혜민화제국방'),
                ('liujunzi-yixuexinwu', 'liujunzi-tang', '백출 진토초')]:
            with self.subTest(formula=fid):
                record = records[fid]
                self.assertEqual(record['dcterms:source']['@id'],
                                 BASE + '/formulas/' + source + '/#source-dose-original')
                self.assertIn(condition, record['skos:scopeNote']['@value'])
                self.assertIn('白朮', record['dcterms:description']['@value'])
                self.assert_public_answer(record, rendered)


    def test_three_phlegm_questions_keep_distinct_qualified_treatment_routes(self):
        expected = {
            'banxia-houpo-jinkui': ('phlegm-qi-binding', 'move-qi-dissipate-binding-transform-phlegm'),
            'liujunzi-yixuexinwu': ('spleen-qi-deficiency-with-phlegm', 'tonify-spleen-transform-phlegm'),
            'wendan-sanyin': ('gallbladder-stomach-disharmony', 'regulate-qi-transform-phlegm-harmonize-stomach'),
        }
        rendered = pattern_treatment_routes(self.payload)
        for fid, (pattern, principle) in expected.items():
            with self.subTest(formula=fid):
                contexts = [n for n in self.records
                            if n['rdf:subject']['@id'] == RESOURCE + '#' + fid
                            and n['rdf:predicate']['@id'] == 'km:hasTraditionalPatternContext'
                            and n['rdf:object']['@id'] == RESOURCE + '#' + pattern]
                self.assertEqual(len(contexts), 1)
                context = contexts[0]
                self.assertEqual(context['rdf:object']['@id'], RESOURCE + '#' + pattern)
                treatments = [n for n in self.records
                              if n['rdf:subject']['@id'] == context['rdf:object']['@id']
                              and n['rdf:predicate']['@id'] == 'km:hasTraditionalTreatmentPrinciple']
                self.assertEqual(len(treatments), 1)
                self.assertEqual(treatments[0]['rdf:object']['@id'], RESOURCE + '#' + principle)
                name = self.nodes[RESOURCE + '#' + fid]['skos:prefLabel']['@value']
                pattern_name = self.nodes[RESOURCE + '#' + pattern]['skos:prefLabel']['@value']
                row = next(r for r in rendered.splitlines()
                           if r.startswith('| <a') and name in r and '>' + pattern_name + '</a>' in r)
                for record in [context, treatments[0]]:
                    self.assertIn(record['dcterms:source']['@id'], row)
                    self.assertIn(record['dcterms:description']['@value'], unescape(row))
                    self.assertIn(record['skos:scopeNote']['@value'], unescape(row))
                    for end in ['rdf:subject', 'rdf:object']:
                        url = self.nodes[record[end]['@id']]['foaf:page']['@id'].split('#')[0]
                        exported = next(n for n in self.pages[url]['payload']['@graph']
                                        if n['@id'] == record['@id'])
                        self.assertEqual(exported, record)

        liujunzi_patterns = {n['rdf:object']['@id'].split('#')[-1] for n in self.records
                             if n['rdf:subject']['@id'] == RESOURCE + '#liujunzi-yixuexinwu'
                             and n['rdf:predicate']['@id'] == 'km:hasTraditionalPatternContext'}
        self.assertEqual(liujunzi_patterns, {'qi-deficiency', 'spleen-qi-deficiency-with-phlegm'})

    def test_shared_herbs_preserve_the_three_different_base_formulations(self):
        def ingredients(fid):
            return {r['rdf:object']['@id'].split('#')[-1] for r in self.records
                    if r['rdf:subject']['@id'] == RESOURCE + '#' + fid
                    and r['rdf:predicate']['@id'] == 'km:containsHerb'}
        banxia, liujunzi, wendan = map(ingredients,
            ['banxia-houpo-jinkui', 'liujunzi-yixuexinwu', 'wendan-sanyin'])
        self.assertEqual(banxia & liujunzi & wendan, {'pinellia', 'poria', 'fresh-ginger'})
        self.assertEqual(banxia - liujunzi - wendan, {'magnolia-bark', 'perilla-leaf'})
        self.assertEqual(liujunzi - banxia - wendan, {'ginseng', 'atractylodes'})
        self.assertEqual(wendan - banxia - liujunzi, {'citrus-immature', 'bamboo-shavings'})
        self.assertEqual([len(banxia), len(liujunzi), len(wendan)], [5, 8, 8])

    def test_missing_qi_binding_principle_does_not_borrow_another_phlegm_treatment(self):
        from copy import deepcopy
        payload = deepcopy(self.payload)
        payload['@graph'] = [n for n in payload['@graph']
                            if not (n.get('rdf:predicate', {}).get('@id') == 'km:hasTraditionalTreatmentPrinciple'
                                    and n['rdf:subject']['@id'] == RESOURCE + '#phlegm-qi-binding')]
        rendered = pattern_treatment_routes(payload)
        self.assertNotIn('반하후박탕 — 금궤요략 수록형', rendered)
        self.assertIn('육군자탕 — 의학심오 수록형', rendered)
        self.assertIn('온담탕 — 삼인극일병증방론 수록형', rendered)


if __name__ == '__main__':
    unittest.main()
