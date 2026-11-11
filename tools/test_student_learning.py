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
        expected = {'anatomy': 620, 'acupoints': 361, 'acupuncture': 169, 'herbs': 184, 'formulas': 110, 'shanghanlun': 70, 'sasang': 48}
        manifest = json.loads((study.OUT / 'manifest.json').read_text())
        for subject, deck in self.decks.items():
            self.assertEqual(len(deck['cards']), expected[subject])
            self.assertEqual(json.loads((study.OUT / (subject + '.json')).read_text()), deck)
            summary = next(s for s in manifest['subjects'] if s['id'] == subject)
            self.assertEqual(summary['questions'], len(deck['questions']))
        self.assertEqual(self.decks, study.build())

    def test_liuwei_url_cleanup_keeps_existing_learning_identity(self):
        deck = self.decks['formulas']
        card = next(c for c in deck['cards'] if c['id'] == 'formula-liu-wei-dihuang-wan')
        self.assertEqual(card['source'], '/formulas/liuwei-dihuang-wan/')
        for question in deck['questions']:
            if question['cardId'] == card['id']:
                source = question.get('relatedSource', question['source'])
                self.assertEqual(source, card['source'])

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
                if q['kind'] != 'clinical':
                    self.assertIn(by_id[q['cardId']]['title'], q['explanation'])
                else:
                    self.assertTrue(q['explanation'] and q['options'][q['answer']]['detail'])
                if q['kind'] in ('advanced', 'clinical'):
                    self.assertEqual(q['source'], '/learning/' + deck['subject'] + '/#' + q['id'])
                    if q.get('topic') in ('statement-comparison', 'conditional-reasoning') and q.get('references'):
                        self.assertIn(q['relatedSource'], [by_id[q['cardId']]['source']] + [r['url'] for r in q['references']])
                    else:
                        self.assertEqual(q['relatedSource'], by_id[q['cardId']]['source'])
                    self.assertTrue(all(o['source'] == q['source'] and o['detail'] for o in q['options']))
                    continue
                for option in q['options']:
                    owner = by_id[option['ownerId']]
                    self.assertEqual(option['source'], owner['source'])
                    self.assertTrue(option['text'] == owner['title'] or option['text'] in [f['value'] for f in owner['facts']])
            self.assertEqual(positions, {0, 1, 2, 3, 4})

    def test_classical_banks_keep_originals_editions_and_interpretive_context(self):
        from collections import Counter
        for subject, count, cases in (('shanghanlun', 70, 36), ('sasang', 48, 24)):
            deck = self.decks[subject]
            self.assertEqual(len(deck['cards']), count)
            self.assertEqual(len(deck['questions']), count * 3 + cases + 34 + 108)
            for c in deck['cards']:
                facts = {f['label']: f['value'] for f in c['facts']}
                self.assertTrue({'우리말 풀이', '판본·범위', '판독 핵심', '치법·처방', '감별·해석'} <= facts.keys())
                self.assertTrue('원문' in facts or '분류 표지어' in facts)
                self.assertIn(c['id'], c['source'])
                self.assertTrue(c['relatedSource'].startswith('/'))
            self.assertEqual(Counter(q['cardId'] for q in deck['questions'] if q['kind'] not in ('advanced', 'clinical')),
                             {c['id']: 4 if any(f['label'] == '증례 독해' for f in c['facts']) else 3 for c in deck['cards']})
            self.assertEqual(sum(q['kind'] == 'case' for q in deck['questions']), cases)
            self.assertTrue(all(q['context'] and all(o['detail'] for o in q['options']) for q in deck['questions']))
        # The archive's selected Song clauses must agree verbatim with the bank.
        for row in json.loads((study.ROOT / 'data/shanghan_learning.json').read_text())['items']:
            source = urlsplit(row['relatedSource'])
            text = (study.DOCS / (source.path.strip('/') + '.md')).read_text()
            fragment = source.fragment
            body = re.search(r'^## .*?\{#' + fragment + r'\}\n(.*?)(?=^## |\Z)', text, re.M | re.S)[1]
            self.assertEqual(row['original'], ' '.join(re.findall(r'^> (.*)', body, re.M)))
        sasang = self.decks['sasang']
        self.assertEqual(Counter(q['kind'] for q in sasang['questions']), {'original': 48, 'interpretation': 48, 'treatment': 28, 'formula': 20, 'case': 24, 'advanced': 34, 'clinical': 108})
        for key in ('soeum', 'soyang', 'taeeum', 'taeyang'):
            self.assertTrue(any(c['id'] == 'sasang-health-' + key for c in sasang['cards']))
        headings = [c for c in sasang['cards'] if c['id'].startswith('sasang-pattern-')]
        self.assertTrue(all('조문 본문 아님' in c['facts'][0]['value'] for c in headings))

    def test_classical_cases_use_close_peers_and_keep_source_layers_separate(self):
        for subject, filename in (('shanghanlun', 'shanghan_learning.json'), ('sasang', 'sasang_learning.json')):
            rows = json.loads((study.ROOT / 'data' / filename).read_text())['items']
            bank = self.decks[subject]
            by_id = {c['id']: c for c in bank['cards']}
            questions = {q['id']: q for q in bank['questions']}
            for r in rows:
                peers = r['compareWith']
                self.assertTrue(peers)
                self.assertTrue(all(p in by_id and p != r['id'] for p in peers))
                # Editorially chosen closest peer must survive category sorting.
                q = questions[r['id'] + '-interpretation']
                self.assertIn(peers[0], {o['ownerId'] for o in q['options']})
                treatment = questions[r['id'] + '-treatment']
                self.assertTrue(set(r.get('treatmentAvoid', [])).isdisjoint(o['ownerId'] for o in treatment['options']))
                if r.get('quizCase'):
                    q = questions[r['id'] + '-case']
                    self.assertEqual(q['context'], r['quizCase'])
                    self.assertEqual(q['options'][q['answer']]['ownerId'], r['id'])
                    self.assertNotIn(r['title'], q['context'])
                    if r['id'].startswith('sasang-detail-'):
                        self.assertTrue(all(o['ownerId'].startswith('sasang-detail-') for o in q['options']))
                if r.get('sourceKind') == 'cpg':
                    facts = {f['label']: f['value'] for f in by_id[r['id']]['facts']}
                    self.assertNotIn('원문', facts)
                    self.assertIn('임상진료지침', facts['판본·범위'])
                    self.assertIn('원전 조문 본문 아님', facts['원문 구분'])
                    self.assertEqual(by_id[r['id']]['referenceLabel'], '병증 임상진료지침·인용 원문')
        sasang = {c['id']: c for c in self.decks['sasang']['cards']}
        self.assertIn('7-30', str(sasang['sasang-detail-taeeum']['facts']))
        self.assertIn('7-30', str(sasang['sasang-detail-soeum']['facts']))
        self.assertIn('동의사상신편(1929)', str(sasang['sasang-formula-dokhwaljihwang-tang']['facts']))

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

    def test_point_names_replace_code_recall_without_losing_point_identity(self):
        code = re.compile(r'\b(?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR|GV|CV)\d+\b')
        for subject in ('acupoints', 'acupuncture'):
            deck = self.decks[subject]
            for c in deck['cards']:
                self.assertFalse(code.search(c['title'] + c['prompt'] + str(c['facts'])), c['id'])
            for q in deck['questions']:
                prose = q['prompt'] + q.get('context', '') + q['explanation'] + ' '.join(o['text'] for o in q['options'])
                self.assertFalse(code.search(prose), q['id'])
        points = self.decks['acupoints']
        by_id = {c['id']: c for c in points['cards']}
        for c in points['cards']:
            self.assertEqual(c['id'], 'point-' + c['code'])
            self.assertIn(c['code'], c['aliases'])
            q = next(q for q in points['questions'] if q['id'] == c['id'] + '-name-혈명·경맥')
            self.assertIn(c['title'], q['prompt'])
            self.assertEqual(q['options'][q['answer']]['text'], c['facts'][1]['value'])
        for id in ('point-LI4-location', 'point-PC6-location', 'point-CV12-location'):
            q = next(q for q in points['questions'] if q['id'] == id)
            self.assertEqual(q['options'][q['answer']]['ownerId'], q['cardId'])
        middle = next(q for q in points['questions'] if q['id'] == 'point-CV12-location')
        owners = {o['ownerId'] for o in middle['options']}
        self.assertTrue({'point-CV11', 'point-CV12', 'point-CV13'} <= owners)
        self.assertTrue(owners <= {'point-CV10', 'point-CV11', 'point-CV12', 'point-CV13', 'point-CV14'})
        self.assertTrue(all(by_id[o['ownerId']]['category'] == middle['category'] for o in middle['options']))

    def test_formula_family_distractors_cross_general_formulary_categories(self):
        formulas = self.decks['formulas']
        for id in ('formula-sijunzi-tang-fact-구조 읽기', 'formula-sijunzi-tang-recall-구조 읽기'):
            q = next(q for q in formulas['questions'] if q['id'] == id)
            self.assertTrue({'formula-liujunzi-tang', 'formula-xiangsha-liujunzi-tang'} <= {o['ownerId'] for o in q['options']})

    def test_anatomy_identification_and_layer_targets_are_unambiguous(self):
        deck = self.decks['anatomy']
        by_id = {c['id']: c for c in deck['cards']}
        self.assertEqual(sum(c['anatomyKind'] == 'muscle' for c in deck['cards']), 245)
        self.assertEqual(sum(q['kind'] == 'diagram' for q in deck['questions']), 37)
        text = (study.DOCS / 'learning/anatomy.md').read_text()
        ns = '{http://www.w3.org/2000/svg}'
        for c in deck['cards']:
            self.assertIn(f'id="{c["id"]}"', text)
            self.assertTrue(c['references'])
        for q in deck['questions']:
            if q['kind'] in ('fact', 'advanced', 'clinical'):
                continue
            self.assertEqual(q['acceptedAnswers'], by_id[q['cardId']]['aliases'])
            self.assertEqual(q['options'][q['answer']]['ownerId'], q['cardId'])
            if q['kind'] == 'identify':
                self.assertFalse(any(study.normalized(a) in study.normalized(q['context']) for a in q['acceptedAnswers']))
        for path in (study.OUT / 'anatomy-diagrams').glob('*.svg'):
            tree = ET.fromstring(path.read_text())
            self.assertFalse(list(tree.iter(ns + 'a')))
            labels = ' '.join(n.text or '' for n in tree.iter(ns + 'text'))
            for c in deck['cards']:
                if c.get('quizDiagram', '').split('#')[0].endswith(path.name):
                    self.assertNotIn(c['title'], labels)
            self.assertFalse(any(n.attrib.get('aria-label') for n in tree.iter()))
        tissue = ET.fromstring((study.OUT / 'anatomy-diagrams/tissue-layers.svg').read_text())
        layers = {n.attrib['id']: n for n in tissue.iter() if n.attrib.get('class') == 'study-target'}
        self.assertEqual(set(layers), {'skin', 'subcutaneous', 'deep-fascia', 'epimysium', 'perimysium', 'endomysium', 'skeletal-muscle'})
        self.assertEqual(layers['perimysium'][0].attrib['r'], '45')
        self.assertEqual(layers['endomysium'][0].attrib['r'], '12')

    def test_expanded_anatomy_preserves_depth_and_important_exceptions(self):
        from collections import Counter
        cards = {c['id']: c for c in self.decks['anatomy']['cards']}
        self.assertEqual(Counter(c['anatomyKind'] for c in cards.values()),
                         {'muscle': 245, 'nerve': 99, 'bone': 98, 'vessel': 77, 'imaging': 66, 'tissue': 25, 'term': 10})
        for c in cards.values():
            if c['anatomyKind'] in ('muscle', 'nerve', 'bone', 'vessel'):
                self.assertGreaterEqual(len(c['facts']), 4, c['id'])
        self.assertIn('기시', {f['label'] for f in cards['anatomy-muscle-supraspinatus']['facts']})
        self.assertIn('총비골부분', str(cards['anatomy-biceps-femoris']['facts']))
        self.assertIn('척골신경', str(cards['anatomy-flexor-digitorum-profundus']['facts']))
        self.assertIn('작은결절', str(cards['anatomy-subscapularis']['facts']))
        self.assertIn('C2 뒤가지', str(cards['anatomy-nerve-greater-occipital']['facts']))
        self.assertIn('피부감각가지는 없', str(cards['anatomy-nerve-anterior-interosseous']['facts']))
        self.assertIn('목정맥구멍', str(cards['anatomy-cranial-accessory']['facts']))
        self.assertIn('산소가 적은', str(cards['anatomy-vessel-pulmonary-arteries']['facts']))
        self.assertIn('산소가 풍부한', str(cards['anatomy-vessel-pulmonary-veins']['facts']))
        self.assertIn('상장간막정맥', str(cards['anatomy-vessel-portal-vein']['facts']))
        self.assertNotIn('주상골', cards['anatomy-bone-navicular-foot']['aliases'])
        self.assertNotIn('긴엄지폄근', cards['anatomy-extensor-hallucis-longus']['aliases'])

    def test_source_parser_does_not_mix_comparator_and_study_tables(self):
        cards = self.decks['acupuncture']['cards']
        comparisons = [c for c in cards if c['category'] == '비교군 읽기']
        self.assertEqual(len(comparisons), 5)
        self.assertFalse(any('Hando' in c['title'] or 'Navarro' in c['title'] for c in cards))
        self.assertEqual(study.first_table('| A | B |\n|---|---|\n| x | y |\n\n### Other\n| bad | row |\n'), [['A', 'B'], ['x', 'y']])

    def test_ultrasound_scope_and_neurovascular_landmarks_remain_connected(self):
        deck = self.decks['anatomy']
        imaging = [c for c in deck['cards'] if c['anatomyKind'] == 'imaging']
        self.assertEqual(len(imaging), 66)
        self.assertFalse(re.search(r'\b(?:CT|MRI)\b|컴퓨터단층|자기공명', json.dumps(imaging, ensure_ascii=False)))
        by_id = {c['id']: c for c in deck['cards']}
        for suffix in ('neuro-lateral-corticospinal', 'vascular-hepatic-veins',
                       'landmark-ischial-spine', 'imaging-us-anisotropy', 'imaging-us-doppler'):
            c = by_id['anatomy-' + suffix]
            self.assertTrue(c['references'])
            self.assertTrue(any(q['cardId'] == c['id'] for q in deck['questions']))
        text = (study.DOCS / 'learning/anatomy.md').read_text()
        self.assertIn('한의학의 기초 해부학', text)
        self.assertNotIn('의학·치의학·한의학', text)
        for anchor in ('neural-pathways', 'vascular-territories', 'bony-landmarks', 'ultrasound-anatomy'):
            self.assertIn('{#' + anchor + '}', text)

    def test_all_uams_muscle_rows_resolve_to_learnable_cards(self):
        coverage = json.loads((study.ROOT / 'data/anatomy_muscle_coverage.json').read_text())
        cards = {c['id']: c for c in self.decks['anatomy']['cards']}
        self.assertEqual(len(coverage['regions']), 7)
        self.assertEqual(len(coverage['rows']), 294)
        self.assertEqual(len(coverage['concepts']), 240)
        self.assertEqual(len({c['cardId'] for c in coverage['concepts'].values()}), 240)
        for row in coverage['rows']:
            self.assertTrue(row['cards'], row['name'])
            for identifier in row['cards']:
                c = cards[identifier]
                self.assertEqual(c['anatomyKind'], 'muscle')
                self.assertTrue(any(r['url'] == coverage['regions'][row['region']]['url'] for r in c['references']))
                # An old collective cross-reference resolves to three distinct muscles.
                if not row['name'].startswith('peroneus mm.'):
                    self.assertIn(row['name'], c['aliases'])
                self.assertTrue(any(q['cardId'] == identifier for q in self.decks['anatomy']['questions']))
        added = [cards[c['cardId']] for c in coverage['concepts'].values() if c['status'] == 'added']
        self.assertEqual(len(added), 155)
        for c in added:
            labels = {f['label'] for f in c['facts']}
            self.assertTrue({'주요 작용', '신경지배', '대표 혈관', '식별·비교', '근육 유형'} <= labels)
            self.assertTrue({'기시', '정지'} <= labels or {'배치·기원', '연결·층'} <= labels)
        self.assertIn('평활근', str(cards['anatomy-internal-anal-sphincter']['facts']))
        self.assertIn('이완', str(cards['anatomy-internal-anal-sphincter']['facts']))
        self.assertIn('C1', str(cards['anatomy-thyrohyoid']['facts']))
        self.assertIn('제1–2 정중신경', str(cards['anatomy-lumbricals-of-hand']['facts']))
        self.assertIn('제1은 안쪽발바닥신경', str(cards['anatomy-lumbricals-of-foot']['facts']))
        self.assertIn('활차신경 IV', str(cards['anatomy-superior-oblique']['facts']))
        self.assertIn('외전신경 VI', str(cards['anatomy-lateral-rectus']['facts']))

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

    def test_self_paced_guidance_and_learning_scope_match_the_current_bank(self):
        hub = (study.DOCS / 'learning/index.md').read_text()
        self.assertIn('{#first-month}', hub)
        self.assertIn('id="first-week"', hub)  # Existing bookmarks keep working.
        self.assertFalse(re.search(r'^\| \d+일 \|', hub, re.M))
        for subject in self.decks:
            self.assertIn(f']({subject}.md)', hub)
            text = (study.DOCS / 'learning' / (subject + '.md')).read_text()
            self.assertFalse(re.search(r'국시원|국가시험|국가고시|kuksiwon', text))
        self.assertFalse(re.search(r'국시원|국가시험|국가고시|kuksiwon|7일 복습', hub))
        per_level = json.loads((study.ROOT / 'data/advanced_learning.json').read_text())['questionsPerLevel']
        self.assertIn(f'중 {per_level}문제·상 {per_level}문제', hub)
        self.assertIn(f"118개 카드·{len(self.decks['shanghanlun']['questions']) + len(self.decks['sasang']['questions'])}문제", hub)

    def test_ultrasound_cases_cover_tracking_measurement_and_doppler_conditions(self):
        deck = self.decks['anatomy']
        new = [q for q in deck['questions'] if q['kind'] == 'advanced'
               and int(q['id'].rsplit('-', 1)[1]) >= 14]
        self.assertEqual(len(new), 8)
        self.assertTrue(all(q['cardId'].startswith('anatomy-imaging-us-') for q in new))
        self.assertEqual(len({q['cardId'] for q in new}), 8)
        text = (study.DOCS / 'learning/anatomy.md').read_text()
        for anchor in ('ultrasound-technique', 'ultrasound-regions',
                       'ultrasound-doppler', 'ultrasound-measurement'):
            self.assertIn('{#' + anchor + '}', text)
        by_id = {c['id']: c for c in deck['cards']}
        for suffix in ('lister', 'guyon', 'femoral-bundle', 'gluteal-tendons',
                       'lcl-biceps', 'tarsal-tunnel', 'plantar-fascia'):
            card = by_id['anatomy-imaging-us-' + suffix]
            self.assertTrue(any(ref['url'].endswith('.pdf') for ref in card['references']))
        measure = next(q for q in new if q['cardId'].endswith('nerve-csa'))
        self.assertIn('경계 기준', measure['options'][measure['answer']]['text'])
        self.assertTrue(any('PMC10395381' in ref['url']
                            for ref in by_id[measure['cardId']]['references']))

    def test_advanced_banks_have_balanced_levels_and_complete_offline_explanations(self):
        from collections import Counter
        rows = json.loads((study.ROOT / 'data/advanced_learning.json').read_text())['questions']
        self.assertEqual(len(rows), 238)
        for subject, deck in self.decks.items():
            questions = [q for q in deck['questions'] if q['kind'] == 'advanced']
            self.assertEqual(Counter(q['difficulty'] for q in questions), {'high': 17, 'expert': 17})
            self.assertEqual({q['answer'] for q in questions}, {0, 1, 2, 3})
            text = (study.DOCS / 'learning' / (subject + '.md')).read_text()
            self.assertEqual(text.count('<!-- ADVANCED_QUESTIONS_START -->'), 1)
            for q in questions:
                self.assertIn('id="' + q['id'] + '"', text)
                self.assertIn(q['context'], text)
                self.assertIn(f'**정답: {q["answer"] + 1}번**', text)
                self.assertIn(q['discriminator'], text)
                self.assertNotEqual(q['nearestWrong'], q['answer'])
                for o in q['options']:
                    self.assertIn(o['text'], text)
                    self.assertIn(o['detail'], text)
            old = {q['id'] for q in deck['questions'] if q['kind'] != 'advanced'}
            self.assertTrue(old.isdisjoint(q['id'] for q in questions))

    def test_focused_bank_counts_accept_legacy_and_validate_overrides(self):
        from clinical_learning import expected_counts
        subjects = ['anatomy', 'sasang']
        legacy = {'questionsPerLevel': 18}
        self.assertEqual(expected_counts(legacy, subjects)[('sasang', 'expert')], 18)
        focused = dict(legacy, questionsPerLevelBySubject={'sasang': 42})
        counts = expected_counts(focused, subjects)
        self.assertEqual(counts[('anatomy', 'high')], 18)
        self.assertEqual(counts[('sasang', 'expert')], 42)
        for bad in ({'typo': 42}, {'sasang': True}, {'sasang': 0}, {'sasang': '42'}, []):
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                expected_counts(dict(legacy, questionsPerLevelBySubject=bad), subjects)

    def test_five_option_cases_keep_scope_tables_and_static_explanations(self):
        from collections import Counter
        payload = json.loads((study.ROOT / 'data/clinical_learning.json').read_text())
        self.assertEqual(payload['questionsPerLevel'], 18)
        self.assertEqual(len(payload['questions']), 672)
        self.assertEqual(len({q['prompt'] for q in payload['questions']}), 672)
        self.assertEqual(len({q['context'] for q in payload['questions']}), 672)
        for subject, deck in self.decks.items():
            cases = [q for q in deck['questions'] if q['kind'] == 'clinical']
            per_level = {'anatomy': 42, 'shanghanlun': 54, 'sasang': 54, 'acupoints': 54, 'acupuncture': 54, 'herbs': 54, 'formulas': 24}.get(subject, 18)
            self.assertEqual(Counter(q['difficulty'] for q in cases), {'high': per_level, 'expert': per_level})
            self.assertEqual({q['id'] for q in cases}, {f'clinical-{subject}-{n:02}' for n in range(1, per_level * 2 + 1)})
            self.assertEqual({q['answer'] for q in cases}, set(range(5)))
            text = (study.DOCS / 'learning' / (subject + '.md')).read_text()
            self.assertEqual(text.count('<!-- CLINICAL_QUESTIONS_START -->'), 1)
            for q in cases:
                self.assertEqual(len(q['options']), 5)
                self.assertIn('id="' + q['id'] + '"', text)
                self.assertIn(q['context'], text)
                self.assertIn(q['discriminator'], text)
                visible = q['context'] + q['prompt'] + ' '.join(o['text'] for o in q['options'])
                self.assertFalse(re.search(r'\b(?:MRI|CT)\b|엑스레이|X-ray|자기공명|컴퓨터단층', visible, re.I))
                for o in q['options']:
                    self.assertIn(o['detail'], text)
                if 'table' in q:
                    self.assertIn(q['table']['caption'], text)
                    for row in q['table']['rows']:
                        self.assertTrue(all(value in text for value in row))

    def test_learning_release_version_and_case_counts_match_public_hub(self):
        manifest = json.loads((study.OUT / 'manifest.json').read_text())
        script = (study.OUT / 'learning.js').read_text()
        config = (study.ROOT / 'mkdocs.yml').read_text()
        version = re.search(r"const VERSION = '([^']+)'", script)[1]
        self.assertEqual(manifest['version'], version)
        self.assertIn('assets/learning/learning.js?v=' + version, config)
        hub = (study.DOCS / 'learning/index.md').read_text()
        self.assertIn('자체 작성한 **672문제(중 336·상 336)**', hub)
        self.assertIn('기초 해부학은 **84문제**', hub)
        self.assertIn('경혈학·침구학·본초학·상한론·사상의학은 각각 **108문제**', hub)

    def test_statement_combinations_have_one_correct_set_and_keep_korean_labels(self):
        from collections import Counter
        from copy import deepcopy
        from clinical_learning import validate_clinical
        rows = [q for deck in self.decks.values() for q in deck['questions']
                if q.get('topic') == 'statement-comparison']
        self.assertEqual(len(rows), 192)
        self.assertEqual(Counter(q['source'].split('/')[2] for q in rows),
                         {'acupoints': 64, 'acupuncture': 64, 'herbs': 64})
        for q in rows:
            validate_clinical(q)
            self.assertEqual(len({study.normalized(o['text']) for o in q['options']}), 5)
            broken = deepcopy(q)
            broken['answer'] = (q['answer'] + 1) % 5
            with self.assertRaises(AssertionError):
                validate_clinical(broken)
            broken = deepcopy(q)
            broken['table']['rows'][0][1] += ' mismatched table'
            with self.assertRaises(AssertionError):
                validate_clinical(broken)
        self.assertNotEqual(study.normalized('ㄱ · ㄴ'), study.normalized('ㄱ · ㄷ'))
        self.assertIn('총 **192문제**(중 96·상 96)', (study.DOCS / 'learning/index.md').read_text())
        points_by_id = {q['id']: q for q in self.decks['acupoints']['questions']}
        self.assertIn('소해(少海)', points_by_id['clinical-acupoints-49']['statements'][2]['reason'])
        self.assertIn('소해(小海)', points_by_id['clinical-acupoints-50']['statements'][2]['reason'])
        for subject in ('acupuncture', 'herbs', 'acupoints'):
            added = [q for q in self.decks[subject]['questions'] if q['kind'] == 'clinical' and 49 <= int(q['id'].rsplit('-', 1)[1]) <= 88]
            self.assertEqual(len(added), 40)
            self.assertEqual(Counter(q['difficulty'] for q in added), {'high': 20, 'expert': 20})
            self.assertEqual({q['answer'] for q in added}, set(range(5)))
            self.assertEqual(len({tuple(sorted(s['text'] for s in q['statements'])) for q in added}), 40)
            for q in added:
                self.assertTrue(q['references'])
                self.assertIn(q['relatedSource'], [r['url'] for r in q['references']])
                for ref in q['references']:
                    self.assertTrue(ref['url'].startswith('/'))
                    path = study.DOCS / (ref['url'].strip('/') + '.md')
                    self.assertTrue(path.exists() or (study.DOCS / ref['url'].strip('/') / 'index.md').exists(), ref)


    def test_conditional_reasoning_batch_preserves_scope_and_traceable_answers(self):
        from collections import Counter
        rows = [q for d in self.decks.values() for q in d['questions']
                if q.get('batch') == 'reasoning-20261105']
        self.assertEqual(len(rows), 60)
        for subject in ('acupuncture', 'herbs', 'acupoints'):
            added = [q for q in rows if q['id'].startswith('clinical-' + subject + '-')]
            self.assertEqual({q['id'] for q in added},
                             {f'clinical-{subject}-{n}' for n in range(89, 109)})
            self.assertEqual(Counter(q['difficulty'] for q in added), {'high': 10, 'expert': 10})
            self.assertEqual(Counter(q['topic'] for q in added),
                             {'statement-comparison': 12, 'conditional-reasoning': 8})
            for q in added:
                self.assertIn(q['relatedSource'], [r['url'] for r in q['references']])
                for ref in q['references']:
                    path = study.DOCS / ref['url'].strip('/')
                    self.assertTrue(path.with_suffix('.md').exists() or (path / 'index.md').exists(), ref)
        combinations = [q for q in rows if q['topic'] == 'statement-comparison']
        self.assertEqual({sum(s['correct'] for s in q['statements']) for q in combinations}, {1, 2, 3})
        self.assertEqual(len({tuple(s['correct'] for s in q['statements']) for q in combinations}), 7)
        by_id = {q['id']: q for q in rows}
        for qid, correct in {
            'clinical-acupoints-101': '천부 9cm / 협백 12cm',
            'clinical-acupoints-102': '간사 6cm / 극문 10cm',
            'clinical-acupoints-103': '하완 6cm / 중완 12cm / 상완 15cm',
            'clinical-acupoints-104': '가시 중점에서 아래 4cm / 아래각에서 위 8cm',
            'clinical-acupuncture-107': 'A 60% / B 40% / 20%포인트',
        }.items():
            q = by_id[qid]
            self.assertEqual(q['options'][q['answer']]['text'], correct)

    def test_clinical_language_rejects_wrong_particles_in_every_text_field(self):
        from copy import deepcopy
        from clinical_learning import validate_clinical_language
        names = [c['title'].split('(')[0] for s in ('acupoints', 'herbs')
                 for c in self.decks[s]['cards']]
        q = next(q for q in self.decks['acupoints']['questions']
                 if q['id'] == 'clinical-acupoints-96')
        paths = [('prompt',), ('context',), ('explanation',), ('discriminator',),
                 ('statements', 0, 'text'), ('statements', 0, 'reason'),
                 ('options', 0, 'text'), ('options', 0, 'detail'),
                 ('table', 'rows', 0, 1), ('references', 0, 'title')]
        for bad in ('여태은', '지창는', '병풍는', '노수은', '백회은',
                    '대추은', '천부은', '중완는', '전중로',
                    '은 肩貞,은 肩井', '고친다.은 肩貞', 'ㄴ:은 肩貞'):
            for path in paths:
                with self.subTest(bad=bad, path=path):
                    broken = deepcopy(q)
                    target = broken
                    for key in path[:-1]:
                        target = target[key]
                    target[path[-1]] = bad + ' 설명이다.'
                    with self.assertRaisesRegex(AssertionError, q['id']):
                        validate_clinical_language(broken, names)
        # 이 is also a demonstrative; verb endings and ㄹ+로 are valid Korean.
        validate_clinical_language({'id': 'valid', 'text':
            '이 근육은 움직인다. 없는 소견을 찾는 문제이다. 여태는 지창은 중완으로 길로'},
            names + ['길'])

    def test_reasoning_feedback_and_same_name_points_stay_complete(self):
        rows = [q for d in self.decks.values() for q in d['questions']
                if q.get('batch') == 'reasoning-20261105']
        for q in rows:
            if q['topic'] != 'statement-comparison':
                continue
            statements = q['statements']
            expected = {i for i, s in enumerate(statements) if s['correct']}
            self.assertEqual(q['explanation'], ' '.join(
                'ㄱㄴㄷ'[i] + ('은 옳다. ' if s['correct'] else '은 다음과 같이 고친다. ')
                + s['reason'] for i, s in enumerate(statements)))
            self.assertEqual(q['discriminator'], ' '.join(s['reason'] for s in statements))
            for option in q['options']:
                mismatches = [i for i in range(3)
                              if (i in option['statementIndices']) != (i in expected)]
                self.assertEqual(option['detail'], ' '.join(
                    f'{"ㄱㄴㄷ"[i]}: {statements[i]["reason"]}'
                    for i in (mismatches or range(3))))
        q = next(q for q in rows if q['id'] == 'clinical-acupoints-96')
        for text in (q['statements'][1]['reason'], q['explanation'], q['discriminator']):
            self.assertIn('소장경 견정은 肩貞', text)
            self.assertIn('담경 견정은 肩井', text)
        self.assertFalse(q['statements'][1]['correct'])

    def test_condition_comparison_counts_match_hub(self):
        from collections import Counter
        payload = json.loads((study.ROOT / 'data/clinical_learning.json').read_text())
        questions = payload['questions']
        comparisons = [q for q in questions if q.get('topic') == 'conditional-reasoning']
        self.assertEqual(Counter(q['subject'] for q in comparisons),
                         {'acupoints': 8, 'acupuncture': 8, 'herbs': 8, 'formulas': 8})
        self.assertEqual(Counter(q['difficulty'] for q in comparisons), {'high': 16, 'expert': 16})
        hub = (study.DOCS / 'learning/index.md').read_text()
        paragraph = next(p for p in hub.splitlines() if p.startswith('**조건 비교 문제**'))
        self.assertIn(f'총 **{len(comparisons)}문제**(중 16·상 16)', paragraph)
        self.assertIn(f'위의 자체 작성 {len(questions)}문제에 포함됩니다', paragraph)

    def test_formula_comparison_answers_match_rendered_choices(self):
        payload = json.loads((study.ROOT / 'data/clinical_learning.json').read_text())
        originals = {q['id']: q for q in payload['questions'] if q['id'].startswith('clinical-formulas-')}
        deck = {q['id']: q for q in self.decks['formulas']['questions']}
        text = (study.DOCS / 'learning/formulas.md').read_text()
        answer_positions = set()
        for number in range(37, 41):
            question_id = f'clinical-formulas-{number}'
            source, question = originals[question_id], deck[question_id]
            self.assertEqual(source['answer'], question['answer'])
            self.assertEqual(source['nearestWrong'], question['nearestWrong'])
            self.assertEqual([o['text'] for o in source['options']], [o['text'] for o in question['options']])
            section = text.split(f'<span id="{question_id}"></span>', 1)[1].split('</details>', 1)[0]
            self.assertIn(f'**정답: {question["answer"] + 1}번**', section)
            for index, option in enumerate(question['options']):
                self.assertIn(f'{index + 1}. {option["text"]}', section)
                self.assertIn(f'- **{index + 1}번:** {option["detail"]}', section)
            answer_positions.add(question['answer'])
        self.assertGreater(len(answer_positions), 1)

    def test_reasoning_editorial_fix_preserves_answer_and_progress_identity(self):
        import hashlib
        payload = json.loads((study.ROOT / 'data/clinical_learning.json').read_text())
        keys = ['id', 'subject', 'cardId', 'difficulty', 'answer', 'nearestWrong',
                'references', 'relatedSource', 'batch', 'format', 'topic']
        projection = [dict(
            {k: q[k] for k in keys},
            options=[{k: o[k] for k in ('text', 'statementIndices') if k in o}
                     for o in q['options']],
            correct=[s['correct'] for s in q.get('statements', [])])
            for q in payload['questions'] if q.get('batch') == 'reasoning-20261105']
        # PR #889 baseline: editorial changes must retain identifiers, sources,
        # answer keys, statement truth values and the order/content of choices.
        self.assertEqual(hashlib.sha256(json.dumps(
            projection, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
            '20223468489bbbd2c5d31d0bd7e68e605d8d5246e1a0f28c9ed9fbe494dc0bf2')

    def test_hard_classical_cases_keep_clause_numbers_and_source_claims_precise(self):
        sh = {q['id']: q for q in self.decks['shanghanlun']['questions'] if q['kind'] == 'advanced'}
        self.assertIn('時時惡風', sh['advanced-shanghanlun-high-05']['context'])
        self.assertIn('170조', sh['advanced-shanghanlun-high-05']['explanation'])
        self.assertIn('更莫復服', sh['advanced-shanghanlun-high-06']['explanation'])
        self.assertEqual(sh['advanced-shanghanlun-high-07']['cardId'], 'shanghan-clause-316')
        q = sh['advanced-shanghanlun-expert-03']
        self.assertIn('소시호탕', q['options'][q['answer']]['text'])
        self.assertIn('방명이 없음', sh['advanced-shanghanlun-expert-04']['explanation'])
        self.assertEqual(sh['advanced-shanghanlun-expert-09']['cardId'], 'shanghan-clause-338')

    def test_expansion_keeps_comparison_context_and_reverse_recall_unambiguous(self):
        points = [c for c in self.decks['acupuncture']['cards'] if c['id'].startswith('shu-point-')]
        self.assertEqual(len(points), 60)
        lu9 = next(c for c in points if c['id'] == 'shu-point-LU9')
        self.assertEqual(lu9['facts'], [{'label': '소속 경맥', 'value': '폐경'}, {'label': '오수혈 분류', 'value': '수(兪)'}])
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
                self.assertTrue(all(by_id[o['ownerId']]['category'] == q['category'] or
                                    o['ownerId'] in by_id[q['cardId']].get('preferredPeers', []) for o in q['options']))
                label, value = q['context'].split(': ', 1)
                self.assertEqual(sum(any(f['label'] == label and study.normalized(f['value']) == study.normalized(value) for f in c['facts']) for c in deck['cards']), 1)
        formulas = {c['id']: c for c in self.decks['formulas']['cards']}
        self.assertIn('인삼', str(formulas['formula-sijunzi-tang']['facts']))
        self.assertIn('자감초', str(formulas['formula-sijunzi-tang']['facts']))
        self.assertEqual(sum(c['category'] == '처방 계열 비교' for c in formulas.values()), 10)


if __name__ == '__main__':
    unittest.main()

