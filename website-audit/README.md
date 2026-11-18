# Website Audit All-in-One: examples

Actor: [`neocraft/website-audit-all-in-one`](https://apify.com/neocraft/website-audit-all-in-one) ·
$0.49 per site (10 pages included), $0.01 per extra page.

| Example | File |
|---|---|
| Python: audit sites, print score, AI-visibility (GEO) score, top priorities, report link | [`python/audit.py`](python/audit.py) |
| Node.js: same | [`node/audit.mjs`](node/audit.mjs) |
| curl + jq: one synchronous call, CI-style gate | [`curl/run-sync.sh`](curl/run-sync.sh) |
| GitHub Actions: fail the build when the score drops or a critical issue appears | [`github-actions/website-audit-ci.yml`](github-actions/website-audit-ci.yml) |
| AI agents / MCP | [`ai-agents-mcp.md`](ai-agents-mcp.md) |

## Output you will use most

The dataset holds one item with `"type": "site"` per audited website and, when `pageRecords` is on (default), one
`"type": "page"` item per crawled page. On the `site` item:

| Field | Meaning |
|---|---|
| `summary.score`, `summary.grade` | Overall score 0-100 and letter grade A-F (score capped at 49 when a critical problem exists) |
| `summary.critical`, `summary.high`, ... | Number of findings per severity |
| `scores.categories.geo` | AI search visibility (GEO) score; pillars in `scores.breakdown.geo` |
| `topPriorities[]` | Up to 5 most important findings: `title`, `severity`, `firstStep`, `whoCanFix` |
| `quickWins[]` | Up to 8 high/medium-impact fixes that take about 5 or 30 minutes |
| `findings[]` | Every finding with `id`, `category`, `severity`, `confidence`, `explanation`, `fixSteps` |
| `changes.scoreDelta`, `changes.new[]`, `changes.fixed[]` | Comparison with the previous audit of the same URL and `monitorId` (null on the first audit) |

The HTML report is stored as `OUTPUT` (and `OUTPUT.pdf` when `"pdf": true`) in the run's default key-value store.

## Useful input fields

`startUrls` (required, `[{"url": "https://..."}]`), `maxPagesPerSite` (default 20; 10 are included in the price),
`language` (`en` / `fr`), `pageRecords`, `pagespeed` (set `false` for a faster and more stable CI gate),
`renderJs` (`auto` / `always` / `never`), `pdf`, `monitorId` (separate history per project),
`alerts` (Slack / webhook, secret input). See the full list on the Actor's **Input** tab.

## GitHub Action

The same call is packaged as a reusable action: [`Neocraft-tools/website-audit-action@v1`](https://github.com/Neocraft-tools/website-audit-action).
