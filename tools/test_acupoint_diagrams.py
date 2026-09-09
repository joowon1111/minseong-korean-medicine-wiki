"""Coverage and integration gates for the 60 five-shu and 25 other point diagrams."""
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET
import acupoint_diagrams as diagrams

ROOT = Path(__file__).resolve().parents[1]


class DiagramTests(unittest.TestCase):
    def test_all_five_shu_and_major_points_have_valid_diagrams(self):
        data = json.loads((ROOT / 'data/acupoint_diagrams.json').read_text())
        points = [p for r in data['regions'] for p in r['points']]
        codes = {p['code'] for p in points}
        shu = set(re.findall(r'\b(?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR)\d+\b', (ROOT / 'docs/acupuncture-specific/five-shu.md').read_text()))
        self.assertEqual(len(points), 85)
        self.assertEqual(len(codes), 85)
        self.assertEqual(len(shu), 60)
        self.assertEqual({p['code'] for p in points if p['five_shu']}, shu)
        for region in data['regions']:
            svg = ET.parse(ROOT / 'docs/assets/acupoint-atlas' / (region['id'] + '.svg'))
            anchors = {a.attrib['id']: a.attrib['href'] for a in svg.iter('{http://www.w3.org/2000/svg}a')}
            self.assertEqual(set(anchors), {p['code'] for p in region['points']})
            for p in region['points']:
                self.assertEqual(anchors[p['code']], '/' + p['path'][:-3] + '/')
                self.assertTrue((ROOT / 'docs' / p['path']).is_file())
                self.assertTrue(0 < p['x'] < 640 and 0 < p['y'] < 660)

    def test_each_document_gets_one_diagram_in_its_existing_location_section(self):
        diagrams.on_pre_build({})
        for path, (_, point) in diagrams.diagram_index().items():
            original = (ROOT / 'docs' / path).read_text()
            page = SimpleNamespace(file=SimpleNamespace(src_uri=path))
            rendered = diagrams.on_page_markdown(original, page, {}, None)
            self.assertEqual(rendered.count(diagrams.MARKER), 1, path)
            self.assertIn('.svg#' + point['code'], rendered)
            # All original headings, text and their order survive the insertion.
            insertion = re.search(r'\n\n<!-- acupoint-location-diagram -->.*?</div>\n', rendered, re.S)
            self.assertIsNotNone(insertion, path)
            self.assertEqual(rendered[:insertion.start()] + rendered[insertion.end():], original, path)
            self.assertEqual(diagrams.on_page_markdown(rendered, page, {}, None), rendered)

    def test_unrelated_pages_unchanged_and_missing_location_fails(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='index.md'))
        self.assertEqual(diagrams.on_page_markdown('hello', page, {}, None), 'hello')
        path = next(iter(diagrams.diagram_index()))
        page.file.src_uri = path
        with self.assertRaisesRegex(ValueError, 'Missing location'):
            diagrams.on_page_markdown('# no location section', page, {}, None)

    def test_atlas_is_at_top_of_treatment_navigation(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        section = config.split('- 침구·치료:\n', 1)[1]
        self.assertEqual(section.splitlines()[1].strip(), '- WHO 표준 361경혈 아틀라스: acupoint-network/standard-atlas.md')
        self.assertEqual(config.count('WHO 표준 361경혈 아틀라스: acupoint-network/standard-atlas.md'), 1)


if __name__ == '__main__':
    unittest.main()
