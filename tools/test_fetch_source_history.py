"""Source-history fetch preserves document history without fetching other refs."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/fetch_source_history.sh'


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()


class FetchSourceHistoryTest(unittest.TestCase):
    def test_unshallow_only_event_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            remote, author, client = base / 'remote.git', base / 'author', base / 'client'
            git(base, 'init', '--bare', str(remote))
            git(base, 'init', '-b', 'main', str(author))
            git(author, 'config', 'user.email', 'test@example.invalid')
            git(author, 'config', 'user.name', 'Test')
            (author / 'page.md').write_text('first\n')
            git(author, 'add', 'page.md')
            git(author, 'commit', '-m', 'first')
            (author / 'page.md').write_text('second\n')
            git(author, 'commit', '-am', 'second')
            git(author, 'branch', 'unrelated')
            git(author, 'branch', 'gh-pages')
            git(author, 'remote', 'add', 'origin', str(remote))
            git(author, 'push', 'origin', 'main', 'unrelated', 'gh-pages')
            git(remote, 'symbolic-ref', 'HEAD', 'refs/heads/main')
            git(remote, 'update-ref', 'refs/pull/123/merge', git(author, 'rev-parse', 'HEAD'))
            git(base, 'clone', '--depth', '1', '--single-branch', remote.as_uri(), str(client))
            self.assertEqual(git(client, 'rev-list', '--count', 'HEAD'), '1')
            # pull_request runs fetch the event's merge ref, rather than every branch.
            env = {**os.environ, 'GITHUB_REF': 'refs/pull/123/merge'}
            for _ in range(2):
                subprocess.run(['bash', str(SCRIPT)], cwd=client, env=env,
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(git(client, 'rev-parse', '--is-shallow-repository'), 'false')
            self.assertEqual(git(client, 'rev-list', '--count', 'HEAD'), '2')
            self.assertEqual(git(client, 'log', '--format=%s', '--', 'page.md').splitlines(),
                             ['second', 'first'])
            self.assertNotIn('origin/unrelated', git(client, 'branch', '-r'))
            # Deployment fetches only the Pages tip, then extends it instead of
            # replacing the branch's existing history with an orphan commit.
            git(client, 'config', 'user.email', 'test@example.invalid')
            git(client, 'config', 'user.name', 'Test')
            git(client, 'fetch', '--no-tags', '--depth=1', 'origin',
                '+refs/heads/gh-pages:refs/remotes/origin/gh-pages')
            pages_before = git(client, 'rev-parse', 'origin/gh-pages')
            (client / 'site').mkdir()
            (client / 'site/index.html').write_text('published\n')
            subprocess.run([sys.executable, '-m', 'ghp_import', '-n', '-p', '-f', 'site'],
                           cwd=client, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(git(client, 'rev-parse', 'gh-pages^'), pages_before)
            self.assertEqual(git(remote, 'rev-parse', 'refs/heads/gh-pages'),
                             git(client, 'rev-parse', 'gh-pages'))


if __name__ == '__main__':
    unittest.main()
