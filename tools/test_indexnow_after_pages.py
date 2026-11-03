import os
import unittest
from unittest.mock import patch

import indexnow_after_pages as indexnow

A = 'a' * 40
B = 'b' * 40
P = 'c' * 40


class IndexNowTest(unittest.TestCase):
    def test_url_mapping_and_deduplication(self):
        urls = indexnow.collect_urls(['docs/index.md', 'docs/a/index.md', 'docs/a.md',
                                      'docs/a.md', 'docs/robots.txt', 'docs/image.png'])
        self.assertEqual(urls, [indexnow.BASE + '/', indexnow.BASE + '/a/',
                                indexnow.BASE + '/robots.txt'])
        self.assertEqual(indexnow.collect_urls(['mkdocs.yml']), [indexnow.BASE + '/'])
        self.assertEqual(indexnow.collect_urls(['tools/example.py']), [])

    @patch.dict(os.environ, {'GITHUB_SHA': B, 'PAGES_SHA': P})
    @patch.object(indexnow, 'save_state')
    @patch.object(indexnow, 'request')
    @patch.object(indexnow, 'read_state', return_value=(A, 'blob'))
    @patch.object(indexnow, 'git', return_value='docs/first.md\ndocs/second.md')
    @patch.object(indexnow.subprocess, 'run')
    @patch.object(indexnow, 'wait_for_pages')
    def test_checkpoint_advances_only_after_submission(self, wait, run, git, state, send, save):
        run.return_value.returncode = 0
        indexnow.main()
        wait.assert_called_once_with(P, B)
        git.assert_called_once_with('diff', '--no-renames', '--name-only', A, B)
        self.assertEqual(send.call_args.kwargs['payload']['urlList'],
                         [indexnow.BASE + '/', indexnow.BASE + '/first/', indexnow.BASE + '/second/'])
        save.assert_called_once_with(B, 'blob')
        send.side_effect = OSError('network error')
        save.reset_mock()
        with self.assertRaises(OSError):
            indexnow.main()
        save.assert_not_called()

    @patch.dict(os.environ, {'GITHUB_SHA': B, 'PAGES_SHA': P})
    @patch.object(indexnow, 'save_state')
    @patch.object(indexnow, 'read_state')
    @patch.object(indexnow, 'wait_for_pages', side_effect=RuntimeError('cancelled'))
    def test_failed_publication_never_notifies(self, wait, state, save):
        with self.assertRaises(RuntimeError):
            indexnow.main()
        state.assert_not_called()
        save.assert_not_called()

    @patch.object(indexnow, 'request')
    @patch.object(indexnow, 'github')
    def test_publication_requires_success_and_matching_marker(self, gh, request):
        gh.return_value = {'workflow_runs': [{'name': 'pages build and deployment', 'head_branch': 'gh-pages',
                                               'head_sha': P, 'run_number': 1, 'run_attempt': 1,
                                               'status': 'completed', 'conclusion': 'success'}]}
        request.return_value = (B + '\n').encode()
        indexnow.wait_for_pages(P, B)
        request.assert_called_once()
        gh.return_value['workflow_runs'][0]['conclusion'] = 'cancelled'
        request.reset_mock()
        with self.assertRaises(RuntimeError):
            indexnow.wait_for_pages(P, B)
        request.assert_not_called()

    @patch.dict(os.environ, {'GITHUB_SHA': B, 'PAGES_SHA': P})
    @patch.object(indexnow, 'save_state')
    @patch.object(indexnow, 'request')
    @patch.object(indexnow, 'read_state', return_value=(A, 'blob'))
    @patch.object(indexnow.subprocess, 'run')
    @patch.object(indexnow, 'wait_for_pages')
    def test_older_revision_does_not_move_checkpoint(self, wait, run, state, request, save):
        run.return_value.returncode = 1
        with self.assertRaises(RuntimeError):
            indexnow.main()
        request.assert_not_called()
        save.assert_not_called()


if __name__ == '__main__':
    unittest.main()
