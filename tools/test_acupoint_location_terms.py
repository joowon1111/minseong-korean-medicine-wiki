"""Guard reviewed transcription fixes and CSV/catalog location consistency."""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORRECTIONS = {'biceps brachiimuscle': 'biceps brachii muscle', 'infra- clavicular fossa': 'infraclavicular fossa', 'epicondyle ofthe humerus': 'epicondyle of the humerus', 'mandibularnotch': 'mandibular notch', 'anteriormedian line': 'anterior median line', 'metacarpophalangealjoint': 'metacarpophalangeal joint', 'between theradius': 'between the radius', 'thyriod cartilage': 'thyroid cartilage', 'thyroid catilage': 'thyroid cartilage', 'sternocleidomastiod muscle': 'sternocleidomastoid muscle', 'aspect of the firearm': 'aspect of the forearm', 'supraspinatous fossa': 'supraspinous fossa', 'F-cun proximallateral': 'F-cun proximal-lateral'}


class LocationTermTests(unittest.TestCase):
    def test_all_361_catalog_locations_match_source(self):
        with (ROOT / 'data/acupoints_416_ccby4.csv').open(encoding='utf-8-sig', newline='') as f:
            source = {r['entity_id']: r for r in csv.DictReader(f)}
        catalog = json.loads((ROOT / 'data/acupoint_catalog.json').read_text())['points']
        self.assertEqual(len(catalog), 361)
        normalize = lambda s: re.sub(r'\s+', ' ', s).strip()
        for code, point in catalog.items():
            self.assertEqual(normalize(source[code]['location_ko']), normalize(point['location_ko']), code)

    def test_reviewed_errors_cannot_return_in_source_or_outputs(self):
        for directory in ('data', 'docs', '_payload/standard_blocks'):
            for path in (ROOT / directory).rglob('*'):
                if path.suffix not in ('.csv', '.json', '.md', '.svg') or not path.is_file():
                    continue
                text = path.read_text(encoding='utf-8')
                for wrong in CORRECTIONS:
                    self.assertNotIn(wrong, text, str(path.relative_to(ROOT)))

    def test_lu3_canonical_term_in_each_publication_layer(self):
        for name in ('data/acupoints_416_ccby4.csv', 'data/acupoint_catalog.json',
                     'docs/acupuncture/points/lu3.md', 'docs/learning/acupoints.md',
                     '_payload/standard_blocks/lu3.md', 'docs/assets/acupoint-3d/points.json',
                     'docs/assets/acupoint-atlas/discovery.json', 'docs/assets/learning/acupoints.json'):
            self.assertIn('biceps brachii muscle', (ROOT / name).read_text(encoding='utf-8'), name)
