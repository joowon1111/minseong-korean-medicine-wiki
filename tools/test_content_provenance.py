"""Provenance must be stable, privacy-preserving and leave source material intact."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

import content_provenance as p
import page_discovery as discovery
from compare_content_reuse import comparison


class ProvenanceTests(unittest.TestCase):
    def test_id_stable_across_body_edits_and_digest_normalizes_whitespace(self):
        self.assertEqual(p.document_id('https://example.org/a/'), p.document_id('https://example.org/a/'))
        self.assertNotEqual(p.document_id('https://example.org/a/'), p.document_id('https://example.org/b/'))
        self.assertEqual(p.digest('눈\n 건강  안내'), p.digest('눈 건강 안내'))
        self.assertNotEqual(p.digest('눈 건강 안내'), p.digest('눈 건강 변경'))

    def test_watermark_keeps_artwork_ids_credits_and_viewbox(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 660"><title>도해</title><g id="BL2"/><text>existing credit</text></svg>'
        output = p.watermark_svg(svg, 'assets/acupoint-atlas/face.svg', {})
        self.assertIn('existing credit', output)
        self.assertIn('id="BL2"', output)
        self.assertEqual(ET.fromstring(output).attrib['viewBox'], '0 0 640 660')
        self.assertEqual(p.watermark_svg(output, 'assets/acupoint-atlas/face.svg', {}), output)
        self.assertIn('wiki.minseong.co.kr', output)
        self.assertNotIn('minseong-provenance-watermark', svg)

    def test_export_digest_excludes_navigation_and_footer(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)/'test.md'; source.write_text('# 본문\n시험 내용')
            page = SimpleNamespace(title='시험', canonical_url='https://example.org/conditions/test/', meta={'description':'시험 설명'},
                file=SimpleNamespace(src_uri='conditions/test.md', dest_uri='conditions/test/index.html',abs_src_path=str(source)))
            config = {'site_url':'https://example.org/', 'site_name':'시험', 'site_dir':temp,'docs_dir':temp}
            files = SimpleNamespace(get_file_from_path=lambda _: None)
            discovery.on_pre_build(config); p.on_pre_build(config)
            content = discovery.on_page_content('<h1>본문</h1><p>시험 내용</p>',page,config,files)
            content = p.on_page_content(content,page,config,files)
            output = discovery.on_post_page('<html><head></head><body><article>'+content+'</article></body></html>',page,config)
            output = p.on_post_page(output,page,config)
            payload = json.loads((Path(temp)/'assets/ai/pages/conditions/test/index.json').read_text())
            self.assertEqual(payload['provenance']['text_sha256'],p.digest(payload['text']))
            self.assertNotIn('80자',payload['text'])
            self.assertIn('archive:document-id',output)
            self.assertIn('data-archive-provenance',output)
            self.assertNotIn('visitor',payload['provenance'])
            from material.plugins.search.plugin import Parser
            search = Parser(); search.feed(content)
            indexed = ''.join(''.join(section.text) for section in search.data)
            self.assertIn('시험 내용', indexed)
            self.assertNotIn(page.archive_provenance['document_id'], indexed)

    def test_local_overlap_detects_copied_paragraph_in_larger_text(self):
        prose = '눈물흘림은 반사성 눈물과 눈물길 배출장애를 구분하고 눈꺼풀의 위치와 눈감김을 함께 살핍니다.'
        result = comparison(prose, '다른 서론입니다. '+prose+' 마무리도 다릅니다.')
        self.assertEqual(result['original_coverage'],1)
        self.assertLess(result['candidate_coverage'],1)
        self.assertEqual(comparison(prose,'독립적으로 작성한 무관한 내용')['shared_shingles'],0)

    def test_samples_are_real_public_prose_and_exclude_tabular_rows(self):
        line = '정상적으로 공개한 설명 문장입니다. '*10
        self.assertEqual(p.search_samples(line),[line.strip()[:110]])
        self.assertEqual(p.search_samples('표\t' + line),[])

    def test_search_batches_cover_documents_without_duplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            p._documents.clear()
            self.addCleanup(p._documents.clear)
            for i in range(25):
                url=f'https://example.org/{i}/'
                p._documents[url]={'url':url,'source_path':'conditions/dry-eye.md' if i==0 else f'conditions/{i}.md','search_samples':['실제 공개 문장']}
            p.on_post_build({'site_dir':temp,'docs_dir':temp,'site_url':'https://example.org/'})
            index=json.loads((Path(temp)/'assets/provenance/search-index.json').read_text())
            rows=[r for b in index['batches'] for r in json.loads((Path(temp)/b['path']).read_text())['documents']]
            self.assertEqual([b['documents'] for b in index['batches']],[24,1])
            self.assertEqual(len({r['url'] for r in rows}),25)
            self.assertEqual(len(index['core_documents']),1)
