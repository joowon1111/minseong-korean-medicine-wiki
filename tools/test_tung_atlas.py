"""Validate Tung atlas point destinations, coverage and integration."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
import build_tung_atlas as atlas

ROOT=Path(__file__).resolve().parents[1]
NS='{http://www.w3.org/2000/svg}'

class TungAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'data/tung_acupuncture.json').read_text())
        cls.regions=cls.data['regions']

    def test_coverage_and_cited_point_sections(self):
        self.assertEqual(len(self.regions),12)
        self.assertEqual(len({r['zone'] for r in self.regions}),7)
        self.assertEqual(sum(len(r['points']) for r in self.regions),50)
        identifiers=[]
        for r in self.regions:
            page=(ROOT/'docs/tung-acupuncture'/(r['id']+'.md')).read_text()
            for point in r['points']:
                identifiers.append(point['id'])
                self.assertEqual(page.count('{#'+point['id']+'}'),1)
                self.assertIn(point['source'],page)
                self.assertIn(point['location'],page)
            self.assertEqual(page.count('<object '),1)
            self.assertIn('data="/assets/tung-atlas/'+r['id']+'.svg"',page)
            self.assertIn('{#clinical}',page)
        self.assertEqual(len(identifiers),len(set(identifiers)))

    def test_svg_links_and_assets_match_the_manifest(self):
        for r in self.regions:
            svg=(ROOT/'docs/assets/tung-atlas'/(r['id']+'.svg')).read_text()
            self.assertEqual(svg,atlas.render(r))
            root=ET.fromstring(svg)
            links={a.attrib['id']:a for a in root.iter(NS+'a')}
            self.assertEqual(set(links),{p['id'] for p in r['points']})
            for p in r['points']:
                self.assertEqual(links[p['id']].attrib['href'],'/tung-acupuncture/'+r['id']+'/#'+p['id'])
                circle=links[p['id']].find(NS+'circle')
                self.assertEqual((float(circle.attrib['cx']),float(circle.attrib['cy'])),(p['x'],p['y']))
                self.assertTrue(0<p['x']<470 and 65<p['y']<610)
            self.assertNotRegex(svg,r'<script\b|javascript:|\bon\w+=|<image\b')
            self.assertIsNotNone(root.find(NS+'desc'))

    def test_hub_navigation_and_location_variants_are_explicit(self):
        hub=(ROOT/'docs/tung-acupuncture/index.md').read_text()
        nav=(ROOT/'mkdocs.yml').read_text().split('- 침구·치료:\n',1)[1].split('  - 통증·증상으로 찾기:',1)[0]
        self.assertIn('동씨침법 · 부위별 아틀라스:',nav)
        for r in self.regions:
            self.assertIn('('+r['id']+'.md)',hub)
            self.assertIn('tung-acupuncture/'+r['id']+'.md',nav)
        lower=(ROOT/'docs/tung-acupuncture/lower-leg.md').read_text()
        self.assertIn('{#location-variants}',lower)
        self.assertIn('음릉천과 겹치는 위치',lower)
        self.assertIn('음릉천 아래 1촌',lower)
        evidence=(ROOT/'docs/acupuncture-integrated/evidence.md').read_text()
        self.assertIn('{#tung-study}',evidence)
        self.assertIn('10.1007/s11726-022-1331-7',evidence)

if __name__=='__main__':unittest.main()
