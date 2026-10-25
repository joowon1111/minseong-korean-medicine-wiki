"""Offline tests: network faults, malformed records, review gates and path boundaries."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import sys
from unittest.mock import patch

RADAR=Path(__file__).parent/'evidence-radar'
sys.path.insert(0, str(RADAR))
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
            row={'title':'Manual acupuncture randomized trial','abstract':'Completed clinical trial with outcomes reported.','pmid':'12345678','study_type':'RCT','evidence_level':'B',
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

class ClinicalGateRegressionTests(unittest.TestCase):
    def test_protocol_overrides_stale_A_rating_in_both_autopilots(self):
        row={'title':'Pharmacoacupuncture for frozen shoulder: protocol for a systematic review and meta-analysis',
             'doi':'10.3831/KPI.2024.27.1.14','study_type':'Systematic review & meta-analysis','evidence_level':'A'}
        for gate in (auto.quality_reasons,v2.reasons):
            self.assertIn('protocol',gate('pharmacopuncture',row,'conditions/frozen-shoulder.md'))
        self.assertEqual(watch.study_type(row['title'],'',[]),'SR/MA protocol')
        self.assertEqual(watch.study_type('Trial protocol','a systematic review informed this protocol',[]),'SR/MA protocol')

    def test_secondary_depression_scale_cannot_override_sleep_population(self):
        mappings=watch.map_conditions('Tiaoshen acupuncture for shift work circadian rhythm sleep-wake disorder',
                                      '84 patients; anxiety and depression scales improved')
        self.assertEqual({m['archive_path'] for m in mappings},{'conditions/insomnia/'})
        self.assertFalse(any(m['code']=='F32' for m in mappings))
        self.assertEqual(watch.map_conditions('Acupuncture for depression','sleep quality improved')[0]['code'],'F32')

    def test_unavailable_title_uses_verifiable_vernacular_field(self):
        xml=b'<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>42843625</PMID><Article><ArticleTitle>[Not Available].</ArticleTitle><VernacularTitle>Revision sobre dispepsia funcional</VernacularTitle></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>'
        with patch.object(watch,'request',side_effect=[(b'{"esearchresult":{"idlist":["42843625"]}}',[]),(xml,[])]):
            rows,errors=watch.fetch_kind('acupuncture','q','a','b',10)
        self.assertEqual(rows[0]['title'],'Revision sobre dispepsia funcional')
        self.assertEqual(rows[0]['title_source'],'VernacularTitle')
        self.assertEqual(rows[0]['article_title'],'[Not Available].')
        self.assertEqual(errors,[])

    def test_combination_pilot_and_scoping_cannot_be_direct_effect_candidates(self):
        from review_rules import review_reasons
        cases=[('Integrated acupuncture-pharmacotherapy for insomnia','Systematic review & meta-analysis','indirect-or-combination'),
               ('Integrated Chinese and Western Medicine for Depression','Systematic review','indirect-or-combination'),
               ('Acupuncture trial','RCT','indirect-or-combination'),
               ('Warm needle acupuncture versus mild moxibustion','RCT','modality-components-review'),
               ('Types and doses of pharmacopuncture: a scoping review','Scoping review','not-completed-effect-study'),
               ('Pharmacopuncture: a pilot trial','RCT','pilot-or-registration-review')]
        for title,design,expected in cases:
            row={'title':title,'abstract':'acupuncture plus usual care' if title=='Acupuncture trial' else '',
                 'study_type':design,'evidence_level':'A','pmid':'12345678'}
            self.assertIn(expected,review_reasons(row))
            for gate in (auto.quality_reasons,v2.reasons):self.assertIn(expected,gate('acupuncture',row,'a.md'))
        self.assertIn('title-missing',review_reasons({'title':'[Not Available].'}))
        self.assertEqual(review_reasons({'title':'Acupuncture for knee osteoarthritis: randomized controlled trial',
                                        'study_type':'RCT','pmid':'12345678','abstract':'Completed trial with outcomes reported.'}),[])

    def test_realistic_batch_routes_records_and_never_writes_docs(self):
        rows=[{'kind':'acupuncture','title':'Acupuncture for shift work sleep-wake disorder: randomized controlled trial',
               'abstract':'Depression scale assessed; body and auricular acupuncture used.',
               'pmid':'42864286','doi':'10.13703/j.0255-2930.20251202-k0003','publication_types':['Randomized Controlled Trial']},
              {'kind':'acupuncture','title':'Acupuncture for knee osteoarthritis: randomized controlled trial',
               'abstract':'Completed four-week trial.', 'pmid':'12345678','doi':'10.1234/example','publication_types':['Randomized Controlled Trial']}]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);docs=root/'docs';(docs/'conditions').mkdir(parents=True)
            for name in ('insomnia','depression','knee-pain'):(docs/'conditions'/f'{name}.md').write_text('# Existing')
            before={p:p.read_bytes() for p in docs.rglob('*.md')};out=root/'out'
            with patch.object(watch,'QUERIES',{'acupuncture':'q'}),patch.object(watch,'fetch_kind',return_value=(rows,[])),patch('sys.argv',['watch','--docs',str(docs),'--outdir',str(out)]),contextlib.redirect_stdout(io.StringIO()):watch.main()
            held=json.loads((out/'hold-queue.json').read_text());candidates=json.loads((out/'high-confidence-candidates.json').read_text())
            self.assertEqual(held[0]['target'],'conditions/insomnia.md')
            self.assertIn('modality-components-review',held[0]['reasons'])
            self.assertEqual(candidates[0]['target'],'conditions/knee-pain.md')
            self.assertIs(candidates[0]['approved'],False)
            self.assertEqual(candidates[0]['effect_certainty'],'not-assessed')
            self.assertEqual(before,{p:p.read_bytes() for p in docs.rglob('*.md')})

    def test_hidden_protocol_and_registered_completed_trial_are_distinguished(self):
        from review_rules import review_reasons
        row={'title':'Mechanism of cognitive processing for acupuncture: randomized controlled study',
             'study_type':'RCT','evidence_level':'B','pmid':'12345678',
             'abstract':'A total of 56 participants will be recruited and randomly assigned.'}
        self.assertIn('protocol', review_reasons(row))
        self.assertIn('protocol', watch.study_type(row['title'],row['abstract'],[]).lower())
        row['abstract']='The protocol was registered. Sixty patients completed the trial and results were analyzed.'
        self.assertNotIn('protocol',review_reasons(row))
        self.assertEqual(watch.study_type('Acupuncture: randomized controlled trial',row['abstract'],[]),'RCT')
