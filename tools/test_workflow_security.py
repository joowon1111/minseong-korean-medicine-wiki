"""Ensure file-derived data cannot become Actions execution source code."""
from pathlib import Path
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
class WorkflowSecurity(unittest.TestCase):
    def test_inline_scripts_do_not_interpolate_actions_expressions(self):
        for file in (ROOT/'.github/workflows').glob('*.yml'):
            workflow=yaml.safe_load(file.read_text())
            for job in workflow['jobs'].values():
                for step in job['steps']:
                    self.assertNotIn('${{',step.get('run',''),str(file))

    def test_indexnow_json_is_passed_as_data(self):
        workflow=yaml.safe_load((ROOT/'.github/workflows/indexnow.yml').read_text())
        submit=next(s for s in workflow['jobs']['indexnow']['steps'] if s.get('name')=='Submit changed URLs to IndexNow')
        self.assertEqual(submit['env']['INDEXNOW_URLS'],'${{ steps.urls.outputs.json }}')
        self.assertIn('json.loads(os.environ["INDEXNOW_URLS"])',submit['run'])
        compile(submit['run'],'IndexNow','exec')

    def test_pull_request_validation_is_read_only(self):
        workflow=yaml.load((ROOT/'.github/workflows/validate.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertIn('pull_request',workflow['on'])
        self.assertNotIn('pull_request_target',workflow['on'])
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        checkout=workflow['jobs']['validate']['steps'][0]
        self.assertEqual(checkout['with']['persist-credentials'],'false')
