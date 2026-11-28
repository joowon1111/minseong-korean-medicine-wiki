"""Practitioner questions must survive export and the public reverse lookup.

These are composition/source questions, not clinical efficacy assessments.
"""
from html import escape
from pathlib import Path
import unittest

from ontology import BASE, RESOURCE, build_ontology, page_projections
from ontology_views import herb_formula_table


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


if __name__ == '__main__':
    unittest.main()
