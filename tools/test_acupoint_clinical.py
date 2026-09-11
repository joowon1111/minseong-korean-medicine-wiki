"""Cross-check clinical coverage against the independent atlas and Saam tables."""
import json
import re
import unittest

import build_acupoint_clinical as clinical

ROOT = clinical.ROOT


class ClinicalCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points = json.loads((ROOT / 'data/acupoint_clinical.json').read_text())['points']
        cls.atlas = json.loads((ROOT / 'data/acupoint_diagrams.json').read_text())
        cls.formulas = json.loads((ROOT / 'data/saam_formulas.json').read_text())['formulas']

    def test_every_standard_point_has_cited_indications_and_assessment(self):
        atlas_points = {p['code']: p for r in self.atlas['regions'] for p in r['points']}
        self.assertEqual(len(atlas_points), 361)
        self.assertEqual(set(self.points), set(atlas_points))
        for code, point in self.points.items():
            with self.subTest(code=code):
                self.assertEqual(point['path'], atlas_points[code]['path'])
                self.assertTrue(point['indications'] and point['actions'] and point['clinical'])
                self.assertTrue(point['source'].startswith('https://'))
                self.assertTrue((ROOT / 'docs' / point['clinical_path']).is_file())
                text = (ROOT / 'docs' / point['path']).read_text()
                self.assertEqual(text.count(clinical.START), 1)
                self.assertEqual(text.count(clinical.END), 1)
                for indication in point['indications']:
                    self.assertIn(indication, text)

    def test_twenty_four_formulas_have_valid_four_point_sets_and_reverse_links(self):
        self.assertEqual(len(self.formulas), 12)
        self.assertEqual(len({f['meridian'] for f in self.formulas}), 12)
        table = (ROOT / 'docs/acupuncture-specific/saam-12-meridians.md').read_text()
        for formula in self.formulas:
            for fields in [('tonify', 'sedate'), ('excess_tonify', 'excess_sedate')]:
                codes = formula[fields[0]] + formula[fields[1]]
                self.assertEqual(len(codes), 4)
                self.assertEqual(len(set(codes)), 4)
                for code in codes:
                    self.assertIn(code, self.points)
                    point = self.points[code]
                    self.assertIn('../' + point['path'], table)
                    text = (ROOT / 'docs' / point['path']).read_text()
                    self.assertIn('saam-12-meridians.md#' + formula['meridian'].lower(), text)
            self.assertIn('{#' + formula['meridian'].lower() + '}', table)

    def test_all_tung_points_have_individual_cited_profiles_at_existing_anchors(self):
        regions = json.loads((ROOT / 'data/tung_acupuncture.json').read_text())['regions']
        count = 0
        for region in regions:
            text = (ROOT / 'docs/tung-acupuncture' / (region['id'] + '.md')).read_text()
            for point in region['points']:
                count += 1
                profile = point['clinical_profile']
                self.assertTrue(profile['indications'] and profile['actions'] and profile['clinical'])
                section = text.split('{#' + point['id'] + '}', 1)[1]
                section = re.split(r'\n#{2,3} ', section)[0]
                self.assertIn(profile['source'], section)
                self.assertEqual(section.count(clinical.START), 1)
        self.assertEqual(count, 50)

    def test_no_stale_or_duplicate_generated_sections(self):
        for path, generated in clinical.outputs().items():
            self.assertEqual(path.read_text(), generated, str(path))

    def test_location_reference_and_non_needling_points_keep_their_distinction(self):
        st17 = self.points['ST17']
        self.assertIn('기준점', st17['indications'][0])
        self.assertIn('침이나 뜸을 시행하지', st17['clinical'])
        self.assertIn('직접 자침하지', self.points['CV8']['clinical'])


if __name__ == '__main__':
    unittest.main()
