"""The parallel browser runner must preserve either check's failure."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'tools/run_parallel_browser_checks.sh'


class ParallelBrowserChecksTest(unittest.TestCase):
    def run_with_failure(self, failing):
        with tempfile.TemporaryDirectory() as tmp:
            node = Path(tmp) / 'node'
            node.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "$CALLS_FILE"\n'
                            'case "$1" in *"$FAIL_TARGET"*) exit 7;; esac\nexit 0\n')
            node.chmod(0o755)
            calls = Path(tmp) / 'calls'
            env = {**os.environ, 'PATH': tmp + os.pathsep + os.environ['PATH'],
                   'CALLS_FILE': str(calls), 'FAIL_TARGET': failing}
            completed = subprocess.run(['bash', str(RUNNER)], cwd=ROOT, env=env,
                                       capture_output=True, text=True, timeout=10)
            return completed.returncode, calls.read_text().splitlines()

    def test_both_checks_succeed(self):
        result, calls = self.run_with_failure('no-matching-script')
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 2)

    def test_either_failure_fails_the_runner_and_both_execute(self):
        for target in ('responsive_reading', 'network_consolidation'):
            with self.subTest(target=target):
                result, calls = self.run_with_failure(target)
                self.assertNotEqual(result, 0)
                self.assertEqual(len(calls), 2)


if __name__ == '__main__':
    unittest.main()
