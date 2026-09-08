"""Use temporary repositories and synthetic credentials; never real tokens."""
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import check_secrets as scan

class SecretChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patch = patch.object(scan, 'ROOT', self.root)
        self.patch.start(); self.addCleanup(self.patch.stop)
        self.git('init', '-q')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)

    def stage(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content if isinstance(content, bytes) else content.encode())
        self.git('add', '--', name)
        return p

    def test_staged_content_cannot_be_hidden_by_clean_worktree(self):
        token = 'ghp_' + 'a' * 36
        path = self.stage('한글 file\nname.txt', token)
        path.write_text('clean worktree')
        for staged in (False, True):
            count, findings = scan.scan(staged)
            self.assertEqual(count, 1)
            self.assertTrue(any(x[2] == 'github-token' for x in findings))
        out = io.StringIO()
        with contextlib.redirect_stdout(out): self.assertEqual(scan.main(['--staged']), 1)
        self.assertNotIn(token, out.getvalue())

    def test_allow_comment_does_not_bypass_detection(self):
        self.stage('test.txt', 'sk-' + 'b'*30 + ' # secret-scan: allow')
        self.assertTrue(scan.scan(False)[1])

    def test_binary_or_invalid_utf8_does_not_hide_ascii_key(self):
        self.stage('data.bin', b'\xff\x00' + b'ghp_' + b'a'*36)
        self.assertTrue(scan.scan(False)[1])

    def test_empty_repo_and_placeholder_are_clean(self):
        self.assertEqual(scan.scan(False), (0, []))
        self.stage('.env.example', 'API_KEY=YOUR_API_KEY\n')
        self.assertEqual(scan.scan(False), (1, []))

    def test_forced_credential_file_is_rejected_without_content(self):
        self.stage('.env', '')
        self.assertEqual(scan.scan(False)[1][0][2], 'forbidden-credential-file')

    def test_git_or_permission_failure_blocks_check(self):
        for error in (PermissionError(), subprocess.CalledProcessError(1, 'git'), ValueError()):
            with patch.object(scan, 'scan', side_effect=error), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(scan.main([]), 2)

    def test_deleted_file_is_not_scanned(self):
        p = self.stage('file.txt', 'hello')
        self.git('rm', '-f', '--', 'file.txt')
        self.assertEqual(scan.scan(True), (0, []))
