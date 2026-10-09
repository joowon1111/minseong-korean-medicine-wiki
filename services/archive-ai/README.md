# Archive AI answer server

The GitHub Pages archive remains static. This optional Cloudflare Worker performs
server-side retrieval and calls OpenAI Responses. No API key is shipped to the browser.
Without a configured, healthy server, the site hides the optional AI generation panel.
Source search, comparison and personal learning remain available.

## Production configuration

Add these **GitHub repository secrets** through Settings → Secrets and variables → Actions:

| Secret | Purpose |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Deploy Workers on the chosen account; scope permissions to that account |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account identifier |
| `OPENAI_API_KEY` | OpenAI project key with Responses access |

Add repository **variable** `ARCHIVE_AI_URL`, the HTTPS Worker base URL,
for example the actual `minseong-archive-ai` workers.dev URL shown in Cloudflare.
Do not include `/answer`, query parameters, credentials or fragments.
The main deployment workflow deploys the Worker when all three secrets exist,
then builds the public URL configuration into the static site. Run “Deploy MkDocs
to GitHub Pages” manually after configuration. The UI independently checks `/health`
before enabling generation. A URL alone does not enable an unconfigured server.

The Worker uses `gpt-4.1-mini`, configurable in `wrangler.jsonc`. Use a Cloudflare
Workers plan whose CPU allowance supports searching the archive corpus; the
free 10 ms CPU limit is not sufficient for this full-corpus retrieval design.
The native rate-limit binding permits three requests per minute per IP.
Cloudflare's limiter is regional and approximate, not a global spending cap.
Set project spending limits/alerts in the OpenAI account separately.

## Data and grounding

Only `{question, kind}` is accepted from the client. Submitted excerpts, URLs,
source IDs and instructions are rejected. The server downloads passage data only
from `https://wiki.minseong.co.kr/assets/archive-tools/passages.json`, caches it
in memory for ten minutes, combines exact matches with bounded AI query expansion,
and passes at most ten excerpts to the answer model. It does not fetch model URLs.

Answers use strict JSON schema. Every factual paragraph must cite one or more
server-issued source IDs. Every cited source must have a quotation that matches
the actual excerpt after Unicode/whitespace normalization. Unrecognized IDs,
invented quotations, uncited paragraphs, refusals and truncated responses are
rejected. This verifies citation integrity, not the truth of every generated claim;
the site displays source links and quotations for reader verification.

Question text is not stored by this code. Requests use `store:false` at OpenAI;
this is not a promise of zero retention by the provider. Worker observability is
disabled and application errors contain generic codes, never provider bodies or
credentials. Only pressing the generation button sends a question to the server
and OpenAI. Cancellation stops browser waiting; an already started provider call
may still incur cost. Searches alone do not send questions to OpenAI.

The server accepts the production origin only, bounds request/response size,
limits model output, times out external requests and fails closed when rate limiting
or credentials are absent. Origin checks are not authentication; direct clients
can send an Origin header, so retain the rate limit and provider budget controls.

## Verification

`node --test tools/test_archive_ai.cjs` checks retrieval, server request handling,
provider payloads, citation validation, failure states and frontend response validation.
`tools/check_archive_ai.cjs` exercises mobile/desktop rendering with controlled
server fixtures. These fixtures do not count as a successful live model call.
Before declaring AI generation live, verify the deployed `/health` and a real
`/answer` call, then open the returned sources and inspect the Korean answer.

Official references: [Responses / structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
[Worker secrets](https://developers.cloudflare.com/workers/configuration/secrets/),
[GitHub Actions deployment](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/),
[Rate limits](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/).
