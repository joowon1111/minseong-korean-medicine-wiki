"""Route coverage, existing point integration and visible navigation gates."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
import build_meridian_routes as renderer

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'
COUNTS = dict(LU=11, LI=20, ST=45, SP=21, HT=9, SI=19, BL=67, KI=27,
              PC=9, TE=23, GB=44, LR=14, CV=24, GV=28)

class MeridianRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = json.loads((ROOT / 'data/meridian_routes.json').read_text())['routes']
        atlas = (ROOT / 'docs/acupoint-network/standard-atlas.md').read_text()
        cls.points = {re.search(r'([A-Z]{2}\d+)$', name)[1]: path
                      for name, path in re.findall(r'\[([^\]]+)\]\(\.\./(acupuncture/points/[^)]+\.md)\)', atlas)}

    def test_fourteen_routes_and_all_361_existing_point_destinations(self):
        self.assertEqual([r['code'] for r in self.routes], list(COUNTS))
        linked = set()
        for route in self.routes:
            code = route['code']
            self.assertEqual((route['first'], route['last']), (code+'1', code+str(COUNTS[code])))
            source = (ROOT / 'docs' / route['path']).read_text()
            table = re.findall(r'\| ([A-Z]{2}\d+) \| \[[^\]]+\]\(\.\./([^\)]+)\) \|', source)
            self.assertEqual([c for c, _ in table], [code+str(i) for i in range(1, COUNTS[code]+1)])
            for c, destination in table:
                self.assertEqual(destination, self.points[c])
                self.assertTrue((ROOT / 'docs' / destination).is_file())
                linked.add(c)
            self.assertEqual(source.count('<object '), 1)
            self.assertIn('data="/assets/meridian-routes/'+code.lower()+'.svg"', source)
            self.assertLess(source.index('<object '), source.index('## 전체 소속 경혈'))
            if code not in ('CV', 'GV'):
                self.assertIn('{#classical-patterns}', source)
                self.assertIn('{#modern-application}', source)
                self.assertIn('**구절을 발췌**', source)
                self.assertIn('{#_2}', source)
            else:
                self.assertNotIn('**시동병', source)
        self.assertEqual(linked, set(self.points))
        self.assertEqual(len(linked), 361)

    def test_svg_markers_links_and_reproducible_assets(self):
        for route in self.routes:
            source = (ROOT / 'docs/assets/meridian-routes' / (route['code'].lower()+'.svg')).read_text()
            self.assertEqual(source, renderer.render(route))
            root = ET.fromstring(source)
            anchors = {a.attrib['id']: a for a in root.iter(NS+'a') if 'id' in a.attrib}
            self.assertEqual(set(anchors), {p['code'] for p in route['points']})
            for p in route['points']:
                self.assertEqual(p['path'], self.points[p['code']])
                self.assertEqual(anchors[p['code']].attrib['href'], '/'+p['path'][:-3]+'/')
                self.assertTrue(0 < p['x'] < 960 and 0 < p['y'] < 740)
            self.assertIsNotNone(root.find(NS+'title'))
            self.assertIsNotNone(root.find(NS+'desc'))
            self.assertNotRegex(source, r'<script\b|\bon\w+=|javascript:|<image\b')

    def test_meridian_sections_visible_immediately_below_atlas(self):
        nav = (ROOT / 'mkdocs.yml').read_text()
        treatment = nav.split('- 침구·치료:\n', 1)[1].split('- 증상·질환:', 1)[0]
        top = treatment.split('  - 통증·증상으로 찾기:', 1)[0]
        self.assertIn('  - 경락·경맥 한눈에 보기:', top)
        self.assertIn('  - 십이경맥 · 몸에서 지나가는 길:', top)
        self.assertIn('  - 임맥·독맥·기경팔맥:', top)
        self.assertIn('  - 특정혈·배혈 원리:', top)
        for route in self.routes:
            self.assertEqual(treatment.count(route['path']), 1)
            self.assertIn(route['path'], top)
        self.assertNotIn('경락·경맥 지식망:', treatment)

if __name__ == '__main__':
    unittest.main()
