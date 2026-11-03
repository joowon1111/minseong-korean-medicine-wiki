#!/usr/bin/env bash
# Keep complete source history for sitemap lastmod without fetching gh-pages,
# unrelated branches, or tags. Checkout has already selected the event commit.
set -eu
if [ "$(git rev-parse --is-shallow-repository)" = true ]; then
  : "${GITHUB_REF:?GitHub event ref is required}"
  git -c protocol.version=2 fetch --no-tags --unshallow origin "$GITHUB_REF"
fi
