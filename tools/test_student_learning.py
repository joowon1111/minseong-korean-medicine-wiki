import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import build_student_learning as study


class StudentLearning(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decks = study.build()

    def test_complete_decks_and_committed_build_agree(self):
        expected = {'acupoints': 361, 'acupuncture': 169, 'herbs': 184, 'formulas': 110}
        manifest = json.loads((study.OUT / 'manifest.json').read_text())
        for subject, deck in self.decks.items():
            self.assertEqual(len(deck['cards']), expected[subject])
            self.assertEqual(json.loads((study.OUT / (subject + '.json')).read_text()), deck)
            summary = next(s for s in manifest['subjects'] if s['id'] == subject)
            self.assertEqual(summary['questions'], len(deck['questions']))
        self.assertEqual(self.decks, study.build())

    def test_every_source_and_diagram_exists(self):
        for deck in self.decks.values():
            records = deck['cards'] + deck['questions']
            for record in records:
                sources = [record['source']] + [o['source'] for o in record.get('options', [])]
                for source in sources:
                    path = study.DOCS / unquote(urlsplit(source).path).strip('/')
                    self.assertTrue(path.with_suffix('.md').exists() or (path / 'index.md').exists(), source)
                for key in ('diagram', 'quizDiagram'):
                    if key in record:
                        path = study.DOCS / urlsplit(record[key]).path.lstrip('/')
                        self.assertTrue(path.exists(), record[key])
                        tree = ET.fromstring(path.read_text())
                        self.assertTrue(any(n.attrib.get('id') == urlsplit(record[key]).fragment for n in tree.iter()))

    def test_answers_are_traceable_and_positions_are_varied(self):
        for deck in self.decks.values():
            by_title = {c['title']: c for c in deck['cards']}
            by_id = {c['id']: c for c in deck['cards']}
            positions = set()
            for q in deck['questions']:
                positions.add(q['answer'])
                self.assertIn(by_id[q['cardId']]['title'], q['explanation'])
                for option in q['options']:
                    owner = by_id[option['ownerId']]
                    self.assertEqual(option['source'], owner['source'])
                    self.assertTrue(option['text'] == owner['title'] or option['text'] in [f['value'] for f in owner['facts']])
            self.assertEqual(positions, {0, 1, 2, 3})

    def test_question_diagrams_have_no_labels_or_answer_descriptions(self):
        ns = '{http://www.w3.org/2000/svg}'
        for path in (study.OUT / 'diagrams').glob('*.svg'):
            tree = ET.fromstring(path.read_text())
            self.assertFalse(list(tree.iter(ns + 'a')), path)
            for point in tree.iter(ns + 'g'):
                if point.attrib.get('class') == 'point':
                    self.assertEqual([c.tag for c in point], [ns + 'circle'])
                    self.assertNotIn('aria-label', point.attrib)
            self.assertEqual(tree.find(ns + 'desc').text, '경혈 위치 연습 — 붉은 점의 위치를 확인하세요.')
            self.assertFalse(any(re.search(r'\b[A-Z]{2}\d+\b', n.text or '') for n in tree.iter(ns + 'text')))
        self.assertEqual(sum(q['kind'] == 'diagram' for q in self.decks['acupoints']['questions']), 361)

    def test_source_parser_does_not_mix_comparator_and_study_tables(self):
        cards = self.decks['acupuncture']['cards']
        comparisons = [c for c in cards if c['category'] == '비교군 읽기']
        self.assertEqual(len(comparisons), 5)
        self.assertFalse(any('Hando' in c['title'] or 'Navarro' in c['title'] for c in cards))
        self.assertEqual(study.first_table('| A | B |\n|---|---|\n| x | y |\n\n### Other\n| bad | row |\n'), [['A', 'B'], ['x', 'y']])

    def test_selected_curriculum_facts_and_no_fabricated_uniform_fields(self):
        herbs = {c['id']: c for c in self.decks['herbs']['cards']}
        self.assertIn('청열윤폐', str(herbs['herb-fritillaria']['facts']))
        self.assertIn('보중익기', str(herbs['herb-jujube-fruit']['facts']))
        self.assertIn('안신익지', str(herbs['herb-ginseng']['facts']))
        self.assertFalse(any(f['label'] == '성미' for f in herbs['herb-ginseng']['facts']))
        self.assertIn('임의로 확정하지', str(herbs['herb-mihudeung']['facts']))
        formulas = {c['id']: c for c in self.decks['formulas']['cards']}
        self.assertIn('소음인', str(formulas['formula-xiangsha-yangwei-tang']['facts']))
        self.assertIn('계지', str(formulas['formula-bawei-dihuang-wan']['facts']))
        self.assertEqual(len([c for c in herbs.values() if c['category'] != '본초 비교·감별']), 120)

    def test_public_counts_and_static_fallback_are_complete(self):
        hub = (study.DOCS / 'learning/index.md').read_text()
        self.assertIn(f"학습카드 {sum(len(d['cards']) for d in self.decks.values()):,}개", hub)
        self.assertIn(f"해설형 문제 {sum(len(d['questions']) for d in self.decks.values()):,}개", hub)
        for subject, deck in self.decks.items():
            text = (study.DOCS / 'learning' / (subject + '.md')).read_text()
            self.assertIn(f"{len(deck['cards'])}개 카드 · {len(deck['questions']):,}문제", text)
            for c in deck['cards']:
                self.assertIn(c['title'], text)
                self.assertIn(c['source'], text)
                for fact in c['facts']:
                    self.assertIn(fact['value'], text)

    def test_expansion_keeps_comparison_context_and_reverse_recall_unambiguous(self):
        points = [c for c in self.decks['acupuncture']['cards'] if c['id'].startswith('shu-point-')]
        self.assertEqual(len(points), 60)
        lu9 = next(c for c in points if c['id'] == 'shu-point-LU9')
        self.assertEqual(lu9['facts'], [{'label': '소속 경맥', 'value': '폐경 LU'}, {'label': '오수혈 분류', 'value': '수(兪)'}])
        herbs = self.decks['herbs']
        comparisons = [c for c in herbs['cards'] if c['category'] == '본초 비교·감별']
        self.assertEqual(len(comparisons), 64)
        self.assertFalse(any(c['title'] == '풍한습을 풀고 통증 통로를 엶 비교·감별' for c in comparisons))
        for q in herbs['questions']:
            c = next(c for c in herbs['cards'] if c['id'] == q['cardId'])
            if c['category'] == '본초 비교·감별' and q['kind'] == 'fact':
                self.assertIn(c['facts'][0]['value'], q['prompt'])
        for subject in ('acupuncture', 'herbs', 'formulas'):
            deck = self.decks[subject]
            by_id = {c['id']: c for c in deck['cards']}
            reverse = [q for q in deck['questions'] if q['kind'] == 'recall']
            self.assertTrue(reverse)
            for q in reverse:
                self.assertEqual(q['options'][q['answer']]['ownerId'], q['cardId'])
                self.assertEqual(len({o['text'] for o in q['options']}), 4)
                self.assertTrue(all(by_id[o['ownerId']]['category'] == q['category'] for o in q['options']))
                label, value = q['context'].split(': ', 1)
                self.assertEqual(sum(any(f['label'] == label and study.normalized(f['value']) == study.normalized(value) for f in c['facts']) for c in deck['cards']), 1)
        formulas = {c['id']: c for c in self.decks['formulas']['cards']}
        self.assertIn('인삼', str(formulas['formula-sijunzi-tang']['facts']))
        self.assertIn('자감초', str(formulas['formula-sijunzi-tang']['facts']))
        self.assertEqual(sum(c['category'] == '처방 계열 비교' for c in formulas.values()), 10)


if __name__ == '__main__':
    unittest.main()
