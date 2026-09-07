# Repository security rules

This repository is public. Treat every committed file, pull request, issue, and workflow log as public information.

## Secrets

- Never add API keys, tokens, passwords, private keys, service-account files, or `.env` files to Git.
- Keep runtime secrets only in GitHub repository or environment secrets. Reference them in Actions as `${{ secrets.NAME }}`; do not place their values in workflow files, command lines, logs, documentation, or examples.
- Use placeholder values such as `YOUR_API_KEY` in examples.
- If a credential is found, stop before committing or pushing. Remove it from the proposed change, rotate it in its issuing service, and review Git history if it may already have been committed.

## Required check before a commit or push

Run `python tools/check_secrets.py`. The check must finish without findings. Do not bypass the check by weakening a detection pattern. A documented false positive may use an adjacent `secret-scan: allow` marker only when it contains no credential value.
