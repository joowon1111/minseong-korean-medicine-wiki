"""Evidence-role and code checks against reviewed source tables and guidelines."""
import json
import unittest

import acupoint_sources as sources


class SourceRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sources.load_sources()
        cls.clinical = json.loads((sources.ROOT / 'data/acupoint_clinical.json').read_text())
        cls.catalog = json.loads((sources.ROOT / 'data/acupoint_catalog.json').read_text())

    def test_standard_metadata_does_not_imply_domestic_indications(self):
        points = self.catalog['points']
        self.assertEqual(len(points), 361)
        for code, point in points.items():
            self.assertTrue(point['standard_reference'].endswith('/' + code))
            self.assertTrue(point['location_ko'])
            self.assertTrue(point['specific_attributes']['existing_summary'])
        # A metadata-only point retains its actual educational source.
        self.assertEqual(points['ST19']['domestic_source_ids'], [])
        self.assertTrue(points['ST19']['coverage']['legacy_education'])
        self.assertFalse(points['ST19']['coverage']['domestic_traditional'])

    def test_guideline_point_sets_match_the_checked_interventions(self):
        expected = {
            'nckm_fd2021': set('ST36 CV12 PC6 ST25 LR3 CV6 CV10 BL20 BL21 SP4'.split()),
            'nckm_lbp2020': set('GV3 GV4 BL23 BL25 BL31 BL32 BL40 BL60 GB34 SP6'.split())}
        for ref, codes in expected.items():
            actual = {c for c, rows in self.data['points'].items() if any(r['source_id'] == ref for r in rows)}
            self.assertEqual(actual, codes)
        for code in ['CV8', 'ST17']:
            self.assertEqual(self.catalog['points'][code]['clinical'], [])
        primary = {c for c, rows in self.data['points'].items()
                   if any(r['source_id'] == 'nckm_insomnia2021' and 'pattern' not in r for r in rows)}
        self.assertEqual(primary, set('GV20 GV24 HT7 PC6 BL62 KI6 SP6 ST36 LR3'.split()))
        ki3 = self.catalog['points']['KI3']['clinical']
        self.assertTrue(any(r.get('pattern') == '음허화왕' for r in ki3))

    def test_classic_groups_and_pairs_are_not_trial_results(self):
        command = {c for c, attrs in self.data['specific_attributes'].items()
                   if any(a['label'] == '사총혈' for a in attrs)}
        self.assertEqual(command, {'ST36', 'BL40', 'LU7', 'LI4'})
        for a, b in [('PC6', 'SP4'), ('SI3', 'BL62'), ('GB41', 'TE5'), ('LU7', 'KI6')]:
            for code, partner in [(a, b), (b, a)]:
                entries = self.catalog['points'][code]['traditional']
                self.assertTrue(any(e.get('related_points') == [partner] for e in entries))
        for p in self.catalog['points'].values():
            self.assertFalse(any(e.get('source_id') in {'hwang2020', 'choi2021'} for e in p['traditional']))
            self.assertFalse(any(e.get('source_id') in {'jung2015', 'kim2014', 'yoon2024', 'kim2020shu'} for e in p['research']))

    def test_replaced_st36_is_supported_by_literature_not_the_location_db(self):
        point = self.clinical['points']['ST36']
        self.assertEqual(point['references'][0]['id'], 'kim2020shu')
        self.assertIn('281', point['references'][0]['locator'])
        self.assertEqual(point['indications'], ['복부팽만', '위완부 통증', '음식 섭취의 불편'])
        self.assertNotIn('americandragon', point['source'])

    def test_citations_include_locators_and_guideline_policies(self):
        refs = self.catalog['references']
        for p in self.catalog['points'].values():
            for layer in ['traditional', 'clinical', 'research']:
                for entry in p[layer]:
                    if 'source_id' not in entry:
                        continue
                    ref = refs[entry['source_id']]
                    self.assertTrue(entry['locator'] and ref['authors'] and ref['institution'])
                    self.assertTrue(ref['url'].startswith('https://'))
                    if layer == 'clinical':
                        self.assertIn('menu_idx=95', ref['policy_url'])
                        self.assertTrue(entry['population'] and entry['intervention'])

    def test_missing_chinese_characters_are_corrected_in_both_datasets(self):
        import csv
        import unicodedata
        manifest = {p['code']: p for p in json.loads((sources.ROOT / 'data/standard_manifest.json').read_text())}
        with (sources.ROOT / 'data/acupoints_416_ccby4.csv').open(encoding='utf-8-sig') as f:
            csv_points = {p['entity_id']: p for p in csv.DictReader(f)}
        expected = {'LU7': '列缺', 'ST6': '頰車', 'GB15': '頭臨泣', 'GB41': '足臨泣', 'TE11': '淸冷淵'}
        self.assertEqual(len(self.data['name_corrections']), 14)
        for fix in self.data['name_corrections']:
            code = fix['code']
            self.assertEqual(manifest[code]['name_zh'], fix['after'])
            self.assertEqual(csv_points[code]['name_zh'], fix['after'])
        for code, name in expected.items():
            self.assertEqual(unicodedata.normalize('NFKC', manifest[code]['name_zh']), unicodedata.normalize('NFKC', name))


if __name__ == '__main__':
    unittest.main()
