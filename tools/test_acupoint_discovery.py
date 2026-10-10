import json
import unittest
from collections import Counter
from pathlib import Path
from build_acupoint_explorer import ROOT, build


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build()
        cls.entries = cls.data['entries']

    def test_scope_and_reproducibility(self):
        self.assertEqual(Counter(e['kind'] for e in self.entries), {'standard':361, 'saam':26, 'tung':50})
        self.assertEqual(len({e['id'] for e in self.entries}), 437)
        self.assertEqual(json.loads((ROOT/'docs/assets/acupoint-atlas/discovery.json').read_text()), self.data)

    def test_local_destinations_and_diagrams_exist(self):
        for e in self.entries:
            for href in [e['href']] + ([e['route']] if e.get('route') else []):
                path = href.split('#')[0].strip('/')
                self.assertTrue((ROOT/'docs'/(path+'.md')).is_file() or (ROOT/'docs'/path/'index.md').is_file(), href)
            for d in e['diagrams']:
                src=d['src'].split('#')[0]
                self.assertTrue((ROOT/'docs'/src.lstrip('/')).is_file(), src)
                svg=(ROOT/'docs'/src.lstrip('/')).read_text()
                anchor=d['src'].partition('#')[2]
                if anchor:self.assertIn('id="'+anchor+'"',svg)

    def test_distinct_systems_and_anatomy_provenance(self):
        lookup={e['id']:e for e in self.entries}
        hegu=lookup['LI4']
        self.assertEqual(hegu['name'],'합곡')
        self.assertIn('골간근',hegu['anatomy'])
        self.assertIn('정중신경',lookup['PC6']['anatomy'])
        self.assertIn('심비골신경',lookup['ST36']['anatomy'])
        linggu=next(e for e in self.entries if e['kind']=='tung' and e['name']=='영골')
        self.assertNotEqual(linggu['id'],hegu['id'])
        self.assertTrue(linggu['href'].startswith('/tung-acupuncture/'))
        self.assertEqual(linggu['anatomy'],'')  # No invented tissue annotation.
        self.assertIn('CC BY 4.0',self.data['location_attribution'])

    def test_prescription_roles_reference_actual_points(self):
        lookup={e['code']:e for e in self.entries if e['kind']=='standard'}
        for entry in self.entries:
            if 'points' not in entry:continue
            self.assertEqual(Counter(p['role'] for p in entry['points']),{'보':2,'사':2})
            self.assertEqual(len({p['code'] for p in entry['points']}),4)
            for p in entry['points']:
                self.assertEqual(p['name'],lookup[p['code']]['name'])
                self.assertEqual(p['href'],lookup[p['code']]['href'])
        lu=next(e for e in self.entries if e['name']=='폐정격')
        self.assertEqual([p['code'] for p in lu['points']],['LU9','SP3','LU10','HT8'])
        for entry in self.entries:
            if entry['id'] in ['saam-cold','saam-heat']:
                self.assertNotIn('points',entry)
                self.assertIn('전수 처방표',entry['assessment'])

if __name__=='__main__':unittest.main()
