"""Coverage and integration gates for all 361 standard acupoint diagrams."""
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET
import acupoint_diagrams as diagrams

ROOT = Path(__file__).resolve().parents[1]


class DiagramTests(unittest.TestCase):
    def test_all_361_standard_points_have_valid_diagrams(self):
        data = json.loads((ROOT / 'data/acupoint_diagrams.json').read_text())
        points = [p for r in data['regions'] for p in r['points']]
        codes = {p['code'] for p in points}
        shu = set(re.findall(r'\b(?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR)\d+\b', (ROOT / 'docs/acupuncture-specific/five-shu.md').read_text()))
        self.assertEqual(len(points), 361)
        self.assertEqual(len(codes), 361)
        atlas = (ROOT / 'docs/acupoint-network/standard-atlas.md').read_text()
        destinations = dict(re.findall(r'\[([^\]]+)\]\(\.\./(acupuncture/points/[^)]+\.md)\)', atlas))
        expected = {re.search(r'([A-Z]+\d+)$', name)[1]: path for name, path in destinations.items()}
        self.assertEqual({p['code']: p['path'] for p in points}, expected)
        self.assertEqual(len(shu), 60)
        self.assertEqual({p['code'] for p in points if p['five_shu']}, shu)
        for region in data['regions']:
            svg = ET.parse(ROOT / 'docs/assets/acupoint-atlas' / (region['id'] + '.svg'))
            anchors = {a.attrib['id']: a.attrib['href'] for a in svg.iter('{http://www.w3.org/2000/svg}a')}
            self.assertEqual(set(anchors), {p['code'] for p in region['points']})
            self.assertEqual(len(anchors), len(region['points']))
            self.assertEqual(len({(p['x'], p['y']) for p in region['points']}), len(region['points']))
            for p in region['points']:
                self.assertEqual(anchors[p['code']], '/' + p['path'][:-3] + '/')
                self.assertTrue((ROOT / 'docs' / p['path']).is_file())
                self.assertTrue(0 < p['x'] < 640 and 0 < p['y'] < 660)
                mark = next(a for a in svg.iter('{http://www.w3.org/2000/svg}a') if a.attrib['id'] == p['code'])
                dot = mark.find('{http://www.w3.org/2000/svg}circle')
                self.assertEqual((float(dot.attrib['cx']), float(dot.attrib['cy'])), (p['x'], p['y']))
            source = ET.tostring(svg.getroot(), encoding='unicode')
            self.assertNotRegex(source, r'<(?:\w+:)?script\b|\bon\w+=|javascript:')

    def test_each_document_gets_one_diagram_in_its_existing_location_section(self):
        diagrams.on_pre_build({})
        map_points = {p['code']: p for p in json.loads((ROOT / 'docs/assets/acupoint-3d/points.json').read_text())['points']}
        for path, (_, point) in diagrams.diagram_index().items():
            original = (ROOT / 'docs' / path).read_text()
            page = SimpleNamespace(file=SimpleNamespace(src_uri=path))
            rendered = diagrams.on_page_markdown(original, page, {}, None)
            self.assertEqual(rendered.count(diagrams.MARKER), 1, path)
            self.assertIn('.svg#' + point['code'], rendered)
            self.assertEqual(rendered.count('href="/acupoint-network/3d-map/?point=' + point['code'] + '"'), 1, path)
            self.assertEqual(map_points[point['code']]['href'], '/' + path.removesuffix('.md') + '/', path)
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

    def test_sequence_stays_within_each_meridian_and_links_real_documents(self):
        from html.parser import HTMLParser

        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links = {}

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'a':
                    self.links[attrs['rel']] = attrs['href']

        groups = {}
        for _, point in diagrams.diagram_index().values():
            meridian, number = re.fullmatch(r'([A-Z]+)(\d+)', point['code']).groups()
            groups.setdefault(meridian, []).append((int(number), point))
        self.assertEqual(len(groups), 14)
        for group in groups.values():
            ordered = [p for _, p in sorted(group)]
            for i, point in enumerate(ordered):
                parser = Links()
                parser.feed(diagrams.sequence_navigation(point))
                expected = {}
                if i > 0:
                    expected['prev'] = '/' + ordered[i - 1]['path'].removesuffix('.md') + '/'
                if i < len(ordered) - 1:
                    expected['next'] = '/' + ordered[i + 1]['path'].removesuffix('.md') + '/'
                self.assertEqual(parser.links, expected, point['code'])

    def test_all_points_link_to_their_parent_and_keep_heading_anchors(self):
        from collections import Counter
        counts = Counter()
        for path, (_, point) in diagrams.diagram_index().items():
            prefix = re.fullmatch(r'([A-Z]+)(\d+)', point['code'])[1]
            counts[prefix] += 1
            route = diagrams.meridian_index()[prefix]
            parent = (ROOT / 'docs' / route['path']).read_text()
            # The parent also links back to this exact canonical point document.
            self.assertIn('../' + path, parent, point['code'])
            heading = '<h1 id="existing-anchor">' + point['name'] + ' ' + point['code'] + '</h1>'
            original = heading + '<p>Original content</p>'
            page = SimpleNamespace(file=SimpleNamespace(src_uri=path))
            rendered = diagrams.on_page_content(original, page, {}, None)
            self.assertEqual(rendered.count(heading), 1)
            self.assertTrue(rendered.endswith('<p>Original content</p>'))
            self.assertIn('href="/' + route['path'].removesuffix('.md') + '/"', rendered)
            self.assertIn(route['title'] + ' ' + prefix, rendered)
            anchor = '_5' if prefix in {'CV', 'GV'} else '_2'
            self.assertIn('href="/meridian-network/#' + anchor + '"', rendered)
            self.assertEqual(diagrams.on_page_content(rendered, page, {}, None), rendered)
        self.assertEqual(dict(counts), dict(LU=11, LI=20, ST=45, SP=21, HT=9, SI=19,
                                          BL=67, KI=27, PC=9, TE=23, GB=44, LR=14, GV=28, CV=24))
        page = SimpleNamespace(file=SimpleNamespace(src_uri='index.md'))
        self.assertEqual(diagrams.on_page_content('<h1>Home</h1>', page, {}, None), '<h1>Home</h1>')

    def test_atlas_is_at_top_of_treatment_navigation(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        section = config.split('- 침구·치료:\n', 1)[1]
        self.assertEqual(section.splitlines()[1].strip(), '- WHO 표준 361경혈 아틀라스: acupoint-network/standard-atlas.md')
        self.assertEqual(config.count('WHO 표준 361경혈 아틀라스: acupoint-network/standard-atlas.md'), 1)


if __name__ == '__main__':
    unittest.main()
