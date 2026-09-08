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
    "generic-secret-assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|secret|password)[\"']?\s*[:=]\s*[\"']?(?!YOUR_|EXAMPLE|REPLACE|\$\{|<)[A-Za-z0-9_./+=-]{16,}"),
}


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, timeout=60).stdout


def indexed_files(staged: bool):
    changed = set(git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR").split(b"\0")) if staged else None
    for entry in git("ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, oid, stage = metadata.split()
        if stage != b"0":
            raise ValueError("unresolved index conflict")
        if changed is None or name in changed:
            yield name.decode("utf-8", "surrogateescape"), oid, mode


def forbidden_file(name: str) -> bool:
    path = Path(name.lower())
    base = path.name
    return (base == ".env" or (base.startswith(".env.") and base != ".env.example")
            or path.suffix in {".pem", ".key", ".p12", ".pfx", ".keystore"}
            or (base.startswith(("credentials", "secrets")) and path.suffix in {".json", ".yaml", ".yml"}))


def scan_text(text: str):
    # Scan whole text once per rule, computing line numbers only on a match.
    # A comment cannot opt a real credential out of scanning.
    for name, pattern in RULES.items():
        for match in pattern.finditer(text):
            yield text.count("\n", 0, match.start()) + 1, name


def scan(staged: bool) -> tuple[int, list]:
    files = list(indexed_files(staged))
    findings = []
    # Read one blob at a time: writing all requests before reading can deadlock
    # on the pipe buffer and retaining all blob contents wastes memory.
    with subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL) as process:
        try:
            for name, oid, mode in files:
                if forbidden_file(name):
                    findings.append((name, 1, "forbidden-credential-file"))
                if mode == b"160000":
                    continue  # A submodule is a commit, not a file in this index.
                process.stdin.write(oid + b"\n")
                process.stdin.flush()
                header = process.stdout.readline().split()
                if len(header) != 3 or header[1] != b"blob":
                    raise ValueError("cannot read indexed blob")
                size = int(header[2])
                content = process.stdout.read(size)
                if len(content) != size or process.stdout.read(1) != b"\n":
                    raise ValueError("incomplete indexed blob")
                text = content.decode("utf-8", errors="replace")
                findings.extend((name, line, rule) for line, rule in scan_text(text))
        finally:
            process.stdin.close()
            process.stdout.close()
        if process.wait() != 0:
            raise ValueError("Git blob reader failed")
    return len(files), findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true", help="scan staged changes from the Git index")
    args = parser.parse_args(argv)
    try:
        count, findings = scan(args.staged)
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"Secret scan could not complete [{type(error).__name__}]; commit/push blocked.", file=sys.stderr)
        return 2
    if findings:
        print("Potential credential patterns found; values are intentionally hidden:")
        for path, line, rule in findings:
            print(f"  {path!r}:{line} [{rule}]")
        return 1
    print(f"Secret scan passed: {count} indexed files, 0 findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
