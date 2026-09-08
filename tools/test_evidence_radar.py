"""Offline tests: network faults, malformed records, review gates and path boundaries."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

RADAR=Path(__file__).parent/'evidence-radar'
def load(name):
    spec=importlib.util.spec_from_file_location(name,RADAR/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
watch=load('pubmed_weekly_watch')
auto=load('evidence_autopilot')
v2=load('evidence_autopilot_v2')

class EvidenceTests(unittest.TestCase):
    def test_network_retries_and_redacted_error(self):
        with patch.object(watch.urllib.request,'urlopen',side_effect=TimeoutError('sensitive URL')),patch.object(watch.time,'sleep') as sleep:
            result,errors=watch.request('https://example.test/api',{'api_key':'placeholder'},retries=2)
        self.assertIsNone(result);self.assertEqual(len(errors),2);sleep.assert_called_once()
        self.assertNotIn('sensitive',json.dumps(errors));self.assertNotIn('api_key',json.dumps(errors))

    def test_malformed_search_data_is_recorded_without_crash(self):
        for body in (b'{',b'[]',b'{}',b'{"esearchresult":{"idlist":[null]}}'):
            with patch.object(watch,'request',return_value=(body,[])):
                rows,errors=watch.fetch_kind('acupuncture','q','2026/01/01','2026/02/01',10)
            self.assertEqual(rows,[]);self.assertEqual(errors[0]['stage'],'esearch')

    def test_empty_results_and_bad_xml(self):
        with patch.object(watch,'request',return_value=(b'{"esearchresult":{"idlist":[]}}',[])) as request:
            self.assertEqual(watch.fetch_kind('acupuncture','q','a','b',10),([],[]))
            request.assert_called_once()
        for xml in (b'<broken',b'<ERROR>bad</ERROR>'):
            with patch.object(watch,'request',side_effect=[(b'{"esearchresult":{"idlist":["12345678"]}}',[]),(xml,[])]):
                rows,errors=watch.fetch_kind('acupuncture','q','a','b',10)
            self.assertEqual(rows,[]);self.assertEqual(errors[0]['stage'],'efetch')

    def test_valid_pubmed_record(self):
        xml=b'<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>12345678</PMID><Article><ArticleTitle>Trial <i>title</i></ArticleTitle><Abstract><AbstractText>Abstract</AbstractText></Abstract></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>'
        with patch.object(watch,'request',side_effect=[(b'{"esearchresult":{"idlist":["12345678"]}}',[]),(xml,[])]):
            rows,errors=watch.fetch_kind('acupuncture','q','a','b',10)
        self.assertEqual(rows[0]['title'],'Trial title');self.assertEqual(errors,[])

    def test_bad_cli_values_rejected_before_requests(self):
        for args in (['--days','-1'],['--retmax','0'],['--docs','/missing-docs']):
            with patch('sys.argv',['watch',*args]),patch.object(watch,'request') as request,contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:watch.main()
                self.assertEqual(error.exception.code,2);request.assert_not_called()

    def test_record_sources_and_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);docs=root/'docs';docs.mkdir();(docs/'a.md').write_text('ok');(root/'private.md').write_text('private')
            for module,read in ((auto,auto.read_first),(v2,v2.first)):
                self.assertEqual(read([str(root/'missing')]),([],None))
                source=root/'records.json';source.write_text('[null,{"title":"valid"},{"evidence_level":{}},{"keywords":42}]')
                self.assertEqual(len(read([str(source)])[0]),1)
                source.write_text('{}');self.assertEqual(read([str(source)])[0],[])
                self.assertEqual(module.resolve(docs,'a/'),docs/'a.md')
                for path in ('../private','a*',{},None):self.assertIsNone(module.resolve(docs,path))

    def test_input_cannot_override_review_flag_or_resolved_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);docs=root/'docs';docs.mkdir();(docs/'a.md').write_text('# A')
            row={'title':'Manual acupuncture randomized trial','pmid':'12345678','study_type':'RCT','evidence_level':'B',
                 'kcd_candidates':[{'archive_path':'a/'}], 'approved':True,'target':'../private.md','kind':'evil','reasons':[]}
            for module,read_name in ((auto,'read_first'),(v2,'first')):
                out=root/module.__name__
                with patch.object(module,'SOURCES',[('acupuncture',['source'])]),patch.object(module,read_name,return_value=([row],'source')),patch('sys.argv',['auto','--docs',str(docs),'--outdir',str(out)]),contextlib.redirect_stdout(io.StringIO()):
                    module.main()
                result=json.loads((out/'high-confidence-candidates.json').read_text())[0]
                self.assertIs(result['approved'],False);self.assertEqual(result['target'],'a.md');self.assertEqual(result['kind'],'acupuncture')

    def test_protocol_and_other_modality_remain_on_hold(self):
        row={'title':'RCT protocol','study_type':'RCT protocol','evidence_level':'P'}
        self.assertIn('protocol',auto.quality_reasons('acupuncture',row,'a.md'))
        self.assertTrue(watch.modality_reasons('electroacupuncture','ordinary massage'))
