"""Exercise the actual redirect script for retired pages and old fragments."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
import network_redirects as redirects

ROOT = Path(__file__).resolve().parents[1]


class ConsolidatedNetworkRedirects(unittest.TestCase):
    def test_retired_sources_are_not_rendered_as_duplicate_articles(self):
        files = [SimpleNamespace(src_uri=source) for source in redirects.load_routes()]
        files += [SimpleNamespace(src_uri='network/condition-expansion-map.md')]
        self.assertEqual([file.src_uri for file in redirects.on_files(files, {})], ['network/condition-expansion-map.md'])

    def test_all_destinations_are_real_and_not_redirect_chains(self):
        routes = redirects.load_routes()
        self.assertEqual(len(routes), 53)
        for source, route in routes.items():
            for target in [route['target'], *route['anchors'].values()]:
                path = target.split('#')[0]
                self.assertTrue((ROOT / 'docs' / path).is_file(), target)
                self.assertNotIn(path, routes)
                self.assertNotIn('##', redirects.public_url(target, 'https://example.test/'))

    def test_actual_javascript_handles_legacy_and_unknown_fragments(self):
        cases = []
        for source, route in redirects.load_routes().items():
            page = redirects.render_redirect(route, 'https://example.test/')
            script = re.search(r'<script>(.*?)</script>', page, re.S).group(1)
            self.assertIn('noindex,follow', page)
            for fragment in ['', 'unknown-fragment', '%malformed', *route['anchors']]:
                expected = redirects.public_url(route['anchors'].get(fragment, route['target']), 'https://example.test/')
                cases.append({'script': script, 'hash': '#' + fragment if fragment else '', 'expected': expected})
        program = '''const vm=require('node:vm'),assert=require('node:assert/strict');
for(const c of JSON.parse(require('node:fs').readFileSync(0,'utf8'))){
let actual;vm.runInNewContext(c.script,{location:{hash:c.hash,replace:u=>actual=u}});
assert.equal(actual,c.expected);assert.equal((actual.match(/#/g)||[]).length,actual.includes('#')?1:0);
}'''
        subprocess.run(['node', '-e', program], input=json.dumps(cases), text=True, check=True, capture_output=True)

    def test_post_build_generates_every_retired_url(self):
        with tempfile.TemporaryDirectory() as directory:
            redirects.on_post_build({'site_dir': directory, 'site_url': 'https://example.test/'})
            for source in redirects.load_routes():
                target = Path(directory) / source.removesuffix('.md') / 'index.html'
                self.assertTrue(target.is_file())
                self.assertIn('location.replace', target.read_text())

    def test_invalid_paths_are_rejected(self):
        for target in ['../secret.md', '/absolute.md', 'https://example.test/', 'file.html']:
            with self.assertRaises(ValueError): redirects.public_url(target, 'https://example.test/')
