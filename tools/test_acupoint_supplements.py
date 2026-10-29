"""Prevent anatomy/combination records from becoming individual acupuncture points."""
import unittest
import csv
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import build_acupoint_supplements as build
import build_ai_knowledge_layer as knowledge
from acupoint_record_types import supplementary_type


class SupplementalRecordsTests(unittest.TestCase):
    def test_source_names_categories_and_generated_documents(self):
        rows, config = build.load_records()
        self.assertEqual(rows['SA2']['name_ko'], '')
        self.assertEqual(rows['SA2']['name_zh'], '')
        self.assertEqual(len([r for r in rows if r.startswith('EX-')]), 48)
        for path, expected in build.outputs().items():
            self.assertEqual(path.read_text(encoding='utf-8-sig'), expected, str(path))
        for code, info in config['records'].items():
            raw = build.render(code, rows[code], info)
            fm, body = knowledge.parse_frontmatter(raw)
            self.assertEqual(fm['status'], '초안')
            self.assertNotIn('last_reviewed', fm)
            self.assertNotIn('nan', fm['title'].lower())
            self.assertIn(rows[code]['location_ko'].strip(), body)
            self.assertNotIn('## 취혈', body)
            self.assertNotIn('## 자침', body)
            self.assertNotIn('경외기혈은 관련', body)
            self.assertEqual(fm['record_type'], rows[code]['category'])

    def test_ai_export_does_not_assign_who_point_codes_to_supplements(self):
        rows, config = build.load_records()
        with patch.object(knowledge, 'DOCS', build.ROOT / 'docs'):
            for code, info in config['records'].items():
                path = build.ROOT / f'docs/acupuncture/extra-points/{code.lower()}.md'
                self.assertEqual(knowledge.entity_type(path), supplementary_type(code))
                fm, _ = knowledge.parse_frontmatter(build.render(code, rows[code], info))
                self.assertNotIn('who_acupoint', knowledge.extract_codes(fm, fm['title'], path))
            path = build.ROOT / 'docs/acupuncture/extra-points/ex-hn3.md'
            self.assertEqual(knowledge.entity_type(path), 'acupoint')
            self.assertEqual(knowledge.extract_codes({}, '인당 EX-HN3', path)['who_acupoint'], ['EX-HN3'])

    def test_new_procedure_data_or_missing_title_requires_review(self):
        rows, config = build.load_records()
        for field, value in [('category', 'acupoint'), ('method', 'new procedure'), ('name_ko', 'invented name')]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'data').mkdir()
                (root / 'data/acupoint_supplements.json').write_text(json.dumps(config))
                modified = {code: dict(row) for code, row in rows.items()}
                modified['SA2'][field] = value
                with (root / 'data/acupoints_416_ccby4.csv').open('w', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(rows['SA2']))
                    writer.writeheader()
                    writer.writerows(modified.values())
                with patch.object(build, 'ROOT', root), self.assertRaises(ValueError):
                    build.load_records()

    def test_standard_atlas_and_discovery_keep_standard_point_count(self):
        manifest = json.loads((build.ROOT / 'data/standard_manifest.json').read_text())
        catalog = json.loads((build.ROOT / 'data/acupoint_catalog.json').read_text())
        self.assertEqual(len(manifest), 361)
        self.assertEqual(len(catalog['points']), 361)
        self.assertFalse(set(catalog['points']) & {f'SA{i}' for i in range(1, 5)})
        self.assertFalse(set(catalog['points']) & {f'AA{i}' for i in range(1, 4)})
