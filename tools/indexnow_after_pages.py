#!/usr/bin/env python3
"""Notify IndexNow only after the matching GitHub Pages publication succeeds.

The checkpoint branch stores the last fully submitted source revision. The Pages
publisher and this script run inside the same serialized deployment job.
"""
import base64
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request

BASE = 'https://wiki.minseong.co.kr'
KEY = 'c9f08cbe667518fc88901d68a49b5450'  # Public IndexNow ownership key.
STATE_BRANCH = 'indexnow-publication-state'
STATE_PATH = 'indexnow-checkpoint.json'
MARKER = 'indexnow-source-revision.txt'
SHA = re.compile(r'^[0-9a-f]{40}$')


def request(url, *, method='GET', payload=None, token=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'minseong-indexnow'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    if data is not None:
        headers['Content-Type'] = 'application/json'
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers, method=method), timeout=30) as response:
        return response.read()


def github(path, *, method='GET', payload=None):
    return json.loads(request('https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + path,
                              method=method, payload=payload, token=os.environ['GITHUB_TOKEN']))


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def collect_urls(paths):
    urls = set()
    for f in paths:
        if not f.startswith('docs/'):
            continue
        rel = f[5:]
        if rel.endswith('.md'):
            rel = rel[:-3]
            if rel == 'index':
                url = BASE + '/'
            elif rel.endswith('/index'):
                url = BASE + '/' + rel[:-6] + '/'
            else:
                url = BASE + '/' + rel + '/'
            urls.add(url)
        elif rel in ('robots.txt', 'llms.txt'):
            urls.add(BASE + '/' + rel)
    if urls or 'mkdocs.yml' in paths:
        urls.add(BASE + '/')
    return sorted(urls)


def wait_for_pages(pages_sha, source_sha, timeout=1200):
    """Require both the exact Pages run's success and its live revision marker."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = github('/actions/runs?head_sha=' + pages_sha + '&per_page=100')
        runs = [r for r in result['workflow_runs'] if r['name'] == 'pages build and deployment'
                and r['head_branch'] == 'gh-pages' and r['head_sha'] == pages_sha]
        if runs:
            latest = max(runs, key=lambda r: (r['run_number'], r['run_attempt']))
            if latest['status'] == 'completed':
                if latest['conclusion'] != 'success':
                    raise RuntimeError('GitHub Pages publication did not succeed: ' + str(latest['conclusion']))
                try:
                    value = request(BASE + '/' + MARKER + '?revision=' + source_sha).decode().strip()
                    if value == source_sha:
                        return
                except (OSError, UnicodeError):
                    pass
        time.sleep(15)
    raise TimeoutError('Timed out waiting for the exact Pages publication and live marker')


def read_state(source_sha):
    try:
        github('/git/ref/heads/' + STATE_BRANCH)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        github('/git/refs', method='POST', payload={'ref': 'refs/heads/' + STATE_BRANCH, 'sha': source_sha})
    try:
        item = github('/contents/' + STATE_PATH + '?ref=' + STATE_BRANCH)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise
    state = json.loads(base64.b64decode(item['content']).decode('utf-8'))
    previous = state['source_sha']
    if not SHA.fullmatch(previous):
        raise ValueError('Invalid IndexNow checkpoint')
    return previous, item['sha']


def save_state(source_sha, blob_sha):
    content = base64.b64encode((json.dumps({'source_sha': source_sha}) + '\n').encode()).decode()
    payload = {'message': 'Record successful IndexNow submission', 'content': content, 'branch': STATE_BRANCH}
    if blob_sha:
        payload['sha'] = blob_sha
    github('/contents/' + STATE_PATH, method='PUT', payload=payload)


def main():
    source_sha = os.environ['GITHUB_SHA']
    pages_sha = os.environ['PAGES_SHA']
    if not SHA.fullmatch(source_sha) or not SHA.fullmatch(pages_sha):
        raise ValueError('Invalid source or Pages commit')
    wait_for_pages(pages_sha, source_sha)
    previous, blob_sha = read_state(source_sha)
    if previous:
        if subprocess.run(['git', 'merge-base', '--is-ancestor', previous, source_sha]).returncode:
            raise RuntimeError('Checkpoint is not an ancestor of this publication; refusing to move it backwards')
        paths = git('diff', '--no-renames', '--name-only', previous, source_sha).splitlines()
    else:
        # First run has no reliable prior checkpoint. Submit all current documents once.
        paths = git('ls-tree', '-r', '--name-only', source_sha, 'docs').splitlines()
    urls = collect_urls(paths)
    for offset in range(0, len(urls), 10000):
        payload = {'host': 'wiki.minseong.co.kr', 'key': KEY,
                   'keyLocation': BASE + '/' + KEY + '.txt', 'urlList': urls[offset:offset + 10000]}
        request('https://api.indexnow.org/indexnow', method='POST', payload=payload)
    save_state(source_sha, blob_sha)
    print('Published revision recorded; URLs submitted:', len(urls))


if __name__ == '__main__':
    main()
