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
