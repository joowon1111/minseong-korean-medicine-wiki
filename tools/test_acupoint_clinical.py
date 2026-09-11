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

    def test_domestic_replacement_has_traceable_sources_without_relabelling_old_claims(self):
        data = json.loads((ROOT / 'data/acupoint_clinical.json').read_text())
        reviewed = {code: p for code, p in self.points.items()
                    if p.get('profile_kind') == 'domestic_review'}
        self.assertEqual(len(reviewed), 27)
        self.assertEqual(sum('americandragon.com' in p['source'] for p in self.points.values()), 324)
        for code, point in reviewed.items():
            with self.subTest(code=code):
                refs = {r['id']: data['references'][r['id']] for r in point['references']}
                self.assertEqual(point['source'], next(iter(refs.values()))['url'])
                for r in point['references']:
                    self.assertTrue(r['locator'] and r['supports'])
                    self.assertTrue(refs[r['id']]['authors'] and refs[r['id']]['doi'])
                for extra in point['additional_evidence']:
                    self.assertIn(extra['source_id'], refs)
                block = (ROOT / 'docs' / point['path']).read_text().split(clinical.START)[1].split(clinical.END)[0]
                self.assertNotIn('americandragon.com', block)
                self.assertNotIn('\ufffd', block)
                for ref in refs.values():
                    self.assertIn(ref['url'], block)

    def test_trial_use_is_not_rendered_as_proven_or_traditional_efficacy(self):
        # Independently checked against Hwang et al. 2020, Table 1.
        expected = {'HT7': ['불면증'], 'KI3': ['급성 발목염좌'],
                    'PC7': ['손목터널증후군'], 'BL40': ['요통'],
                    'CV12': ['과민성장증후군'], 'LI11': ['고혈압', '급성 뇌졸중']}
        for code, indications in expected.items():
            point = self.points[code]
            self.assertEqual(point['indications'], indications)
            self.assertEqual(point['indications_label'], '임상시험에서 사용된 분야')
            self.assertEqual(point['actions_label'], '자료의 의미')
            self.assertIn('치료 효과를 평가한 결과는 아닙니다', point['actions'][0])
        trials = [p for p in self.points.values() if p.get('indications_label') == '임상시험에서 사용된 분야']
        self.assertEqual(len(trials), 22)

    def test_sp3_has_literature_indications_and_no_invented_institutional_endorsement(self):
        point = self.points['SP3']
        self.assertEqual(point['indications'], ['복부팽만', '복통', '소화불량', '구토', '변비'])
        self.assertEqual(point['indications_label'], '문헌상 주치')
        self.assertEqual(point['references'][0]['id'], 'kim2014')
        self.assertIn('184', point['references'][0]['locator'])

    def test_taegeuk_reuses_source_types_and_portal_reports_actual_coverage(self):
        profiles = (ROOT / 'docs/taegeuk-acupuncture/points.md').read_text()
        for code in ['HT7', 'LU9', 'LR3', 'KI3', 'SP3', 'LI4']:
            section = profiles.split('{#' + code.lower() + '}', 1)[1].split('\n### ', 1)[0]
            self.assertIn(self.points[code]['indications_label'], section)
            self.assertNotIn('americandragon.com', section)
        portal = (ROOT / 'docs/portal/acupuncture.md').read_text()
        self.assertIn('27경혈', portal)
        self.assertIn('303경혈', portal)
        self.assertIn('같은 421개 임상시험', portal)


if __name__ == '__main__':
    unittest.main()
