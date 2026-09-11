"""Guard clinically significant Taegeuk assignments and archive integration."""
import csv
import json
import re
import unittest

import build_acupoint_clinical as clinical
import build_taegeuk as taegeuk

ROOT = taegeuk.ROOT


class TaegeukTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'data/taegeuk_formulas.json').read_text())
        cls.atlas = json.loads((ROOT / 'data/acupoint_clinical.json').read_text())['points']

    def test_assignments_match_2019_table_1_and_2022_guideline_page_128(self):
        # Independently transcribed from the two cited tables; LI4 is not KI3.
        expected = {
            'taeyangin': (['HT8', 'LR3'], ['LU9']),
            'taeeumin': (['HT4', 'LU9'], ['LR3']),
            'soyangin': (['HT3', 'KI3'], ['SP3']),
            'soeumin': (['HT7', 'SP3'], ['LI4']),
        }
        formulas = self.data['formulas']
        self.assertEqual(len(formulas), 4)
        self.assertEqual({f['id'] for f in formulas}, set(expected))
        used = set()
        for f in formulas:
            self.assertEqual((f['tonify'], f['sedate']), expected[f['id']])
            self.assertEqual(f['heart'], f['tonify'][0])
            self.assertTrue(f['source'].startswith('https://'))
            used.update(f['tonify'] + f['sedate'])
        self.assertEqual(used, set(self.data['points']))
        self.assertEqual(len(used), 9)

    def test_only_nine_relevant_atlas_pages_have_correct_reverse_roles(self):
        roles = clinical.taegeuk_roles(self.data['formulas'])
        for code, point in self.atlas.items():
            text = (ROOT / 'docs' / point['path']).read_text()
            self.assertEqual('태극침법에서의 활용' in text, code in roles, code)
            for label, anchor in roles.get(code, []):
                self.assertIn(f'[{label}](../../taegeuk-acupuncture/constitutions.md#{anchor})', text)
        for path, output in clinical.outputs().items():
            self.assertEqual(path.read_text(), output, str(path))

    def test_point_properties_match_independent_special_point_tables(self):
        five_shu = (ROOT / 'docs/meridian-network/special-points/five-shu.md').read_text()
        heart_row = next(line for line in five_shu.splitlines() if line.startswith('| 심 HT |'))
        self.assertEqual(re.findall(r'HT\d+', heart_row), ['HT9', 'HT8', 'HT7', 'HT4', 'HT3'])
        self.assertNotIn('LI4', five_shu)
        for code in ['HT7', 'LU9', 'LR3', 'KI3', 'SP3', 'LI4']:
            self.assertIn('원혈', self.data['points'][code]['specific'])
        for code, point in self.data['points'].items():
            self.assertTrue((ROOT / 'docs' / point['meridian_path']).is_file())
        with (ROOT / 'data/acupoints_416_ccby4.csv').open() as stream:
            row = next(row for row in csv.reader(stream) if row[0] == 'HT4')
        self.assertEqual(row[3], '靈道')
        self.assertIn('**靈道**', (ROOT / 'docs/acupuncture/points/ht4.md').read_text())

    def test_generated_tables_cover_all_points_and_keep_existing_profiles(self):
        for path, output in taegeuk.outputs().items():
            self.assertEqual(path.read_text(), output, str(path))
        profiles = (ROOT / 'docs/taegeuk-acupuncture/points.md').read_text()
        for code in self.data['points']:
            point = self.atlas[code]
            self.assertEqual(profiles.count('{#' + code.lower() + '}'), 1)
            self.assertIn('../' + point['path'], profiles)
            self.assertIn(point['source'], profiles)
            for indication in point['indications']:
                self.assertIn(indication, profiles)

    def test_menu_is_after_all_tung_children_before_mps(self):
        nav = (ROOT / 'mkdocs.yml').read_text().split('- 침구·치료:\n', 1)[1]
        starts = [nav.index('  - ' + name) for name in [
            '사암침법 핵심 지식망:', '동씨침법 · 부위별 아틀라스:',
            '태극침법 핵심 지식망:', '근육·근막·MPS 해부 아틀라스:']]
        self.assertEqual(starts, sorted(starts))
        self.assertEqual(len(re.findall(r'tung-acupuncture/[^\s]+\.md', nav[starts[1]:starts[2]])), 13)
        taegeuk_nav = nav[starts[2]:starts[3]]
        pages = sorted((ROOT / 'docs/taegeuk-acupuncture').glob('*.md'))
        self.assertEqual(len(pages), 6)
        for page in pages:
            self.assertEqual(taegeuk_nav.count('taegeuk-acupuncture/' + page.name), 1)


if __name__ == '__main__':
    unittest.main()
