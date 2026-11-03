#!/usr/bin/env bash
# Run independent, read-only browser checks concurrently; preserve either failure.
set -u
node tools/check_responsive_reading.cjs &
responsive_pid=$!
node tools/check_network_consolidation.cjs &
network_pid=$!
trap 'kill "$responsive_pid" "$network_pid" 2>/dev/null || true' INT TERM
result=0
if wait "$responsive_pid"; then
  echo 'Responsive reading checks passed.'
else
  echo 'Responsive reading checks failed.' >&2
  result=1
fi
if wait "$network_pid"; then
  echo 'Network consolidation checks passed.'
else
  echo 'Network consolidation checks failed.' >&2
  result=1
fi
exit "$result"
