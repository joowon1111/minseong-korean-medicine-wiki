# Repository security rules

This repository is public. Treat every committed file, pull request, issue, and workflow log as public information.

## Secrets

- Never add API keys, tokens, passwords, private keys, service-account files, or `.env` files to Git.
- Keep runtime secrets only in GitHub repository or environment secrets. Reference them in Actions as `${{ secrets.NAME }}`; do not place their values in workflow files, command lines, logs, documentation, or examples.
- Use placeholder values such as `YOUR_API_KEY` in examples.
- If a credential is found, stop before committing or pushing. Remove it from the proposed change, rotate it in its issuing service, and review Git history if it may already have been committed.

## Required check before a commit or push

Run `python tools/check_secrets.py` after staging and before every commit or push.
It checks the actual Git index; `--staged` checks only staged changes. The check
must finish without findings. Never bypass a finding with inline allow markers
or weaker patterns. Any false positive must be reviewed without exposing values.
A failed or incomplete security check blocks publication; do not silently pass it.

## Content integration

- Read the whole target document before expanding it. Integrate new material into the relevant existing paragraphs, tables, and sections; merge or replace overlapping explanations.
- Do not accumulate unrelated update blocks, repeated warnings, link lists, or duplicate summaries at the end of a page. Add a section only when it serves a distinct question in the document's reading order.
- Place related links where readers need the next explanation. Keep the established taxonomy and URLs; verify existing heading anchors when restructuring.
- Prefer strengthening existing documents to creating overlapping pages. Preserve the policy against blanket public review dates and do not invent clinical experience, authorship, or credentials.
