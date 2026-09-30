"""Protect source provenance, reader URLs and isolation from normal search."""
import hashlib,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/assets/donguibogam'
class CorpusTests(unittest.TestCase):
 def test_provenance_and_checksums(self):
  manifest=json.loads((BASE/'manifest.json').read_text());self.assertEqual(manifest,json.loads((ROOT/'data/donguibogam/source-manifest.json').read_text()))
  ids=set();sources={s['id']:s for s in manifest['sources']}
  self.assertFalse(manifest['coverage']['mediclassics_content_used']);self.assertFalse(manifest['coverage']['full_text_complete']);self.assertFalse(manifest['coverage']['facsimiles_hosted_locally'])
  for name,group in manifest['groups'].items():
   file=BASE/group['file'];self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),group['sha256']);rows=json.loads(file.read_text());self.assertEqual(len(rows),group['count'])
   for row in rows:
    self.assertNotIn(row['id'],ids);ids.add(row['id']);self.assertEqual(row['group'],name);self.assertIn(row['source'],sources);self.assertTrue(row['text'].strip())
    for link in row['links']:self.assertTrue((ROOT/'docs'/link['url'].strip('/')).with_suffix('.md').exists())
  self.assertEqual(len(ids),1580)
  for source in sources.values():self.assertEqual(source['license'],'CC-BY-SA-4.0');self.assertIn('oldid='+str(source['revision']),source['url']);self.assertNotIn('mediclassics',source['url'])
 def test_text_is_not_embedded_in_main_search_or_markdown_pages(self):
  page=(ROOT/'docs/classics/donguibogam/original.md').read_text();self.assertIn('exclude: true',page)
  script=(ROOT/'docs/assets/korean-search-185.js').read_text();self.assertNotIn('tangaek-1.json',script);self.assertNotIn('manifest.json',script)
  bootstrap=(BASE/'bootstrap.js').read_text();self.assertIn('if(!root || root.dataset.dgbReady)return',bootstrap)
 def test_source_alias_location_and_published_deep_links(self):
  rows=[r for group in json.loads((BASE/'manifest.json').read_text())['groups'].values() for r in json.loads((BASE/group['file']).read_text())]
  by_id={r['id']:r for r in rows}
  import re
  for page in (ROOT/'docs/classics/donguibogam').rglob('*.md'):
   for key in re.findall(r'original\.md\?record=([a-z0-9-]+)',page.read_text(encoding='utf-8-sig')):self.assertIn(key,by_id)
  angelica=next(r for r in rows if r['title']=='當歸');self.assertEqual(angelica['group'],'tangaek-3')
