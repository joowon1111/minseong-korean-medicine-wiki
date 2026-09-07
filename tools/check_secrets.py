#!/usr/bin/env python3
"""Fail safely when tracked text files contain common credential formats.

The output intentionally names only a file, line, and rule: it never prints a possible secret value. Scan the staged snapshot with --staged before committing.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "private-key": re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "aws-access-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "google-api-key": re.compile(r"\bAIza[\w-]{30,}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "generic-secret-assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[\"']?(?!YOUR_|EXAMPLE|REPLACE|\$\{|<)[A-Za-z0-9_./+=-]{16,}"),
}


def tracked_files(staged: bool) -> list[Path]:
    command = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged else ["git", "ls-files"]
    result = subprocess.run(command, cwd=ROOT, text=True, check=True, capture_output=True)
    return [ROOT / line for line in result.stdout.splitlines()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true", help="scan files staged for the next commit")
    args = parser.parse_args()
    files = tracked_files(args.staged)
    findings: list[tuple[str, int, str]] = []
    for path in files:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if "secret-scan: allow" in line:
                continue
            for name, pattern in RULES.items():
                if pattern.search(line):
                    findings.append((path.relative_to(ROOT).as_posix(), number, name))
    if findings:
        print("Potential credential patterns found; values are intentionally hidden:")
        for path, line, rule in findings:
            print(f"  {path}:{line} [{rule}]")
        return 1
    scope = "staged files" if args.staged else "tracked files"
    print(f"Secret scan passed: {len(files)} {scope}, 0 findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
