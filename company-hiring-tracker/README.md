# Company Hiring Tracker: examples

Actor: [`neocraft/company-hiring-tracker`](https://apify.com/neocraft/company-hiring-tracker) ·
$0.004 per covered company + $0.001 per returned job (every open job in `snapshot` mode; only new / changed /
reopened jobs in `changes` mode). Companies that are not found or not covered, the coverage report, and closed or
unchanged jobs in `changes` mode are free.

| Example | File |
|---|---|
| Python: company summaries + latest jobs | [`python/hiring.py`](python/hiring.py) |
| Node.js: same | [`node/hiring.mjs`](node/hiring.mjs) |
| curl + jq: one synchronous call in `changes` mode | [`curl/run-sync.sh`](curl/run-sync.sh) |
| GitHub Actions: weekly check of a company list, new jobs posted to Slack | [`github-actions/weekly-hiring-slack.yml`](github-actions/weekly-hiring-slack.yml) |
| AI agents / MCP | [`ai-agents-mcp.md`](ai-agents-mcp.md) |

## Input

`companies` accepts names (`"Stripe"`), domains (`"doctolib.fr"`), careers-page or job-board URLs
(`"https://boards.greenhouse.io/airbnb"`) or objects `{"name", "domain", "careersUrl", "ats", "board"}`.
`presetLists` adds ready-made lists (`cac40`, `dax40`, `ftse100`, `fortune100`, `eu_unicorns`, `ai_startups`).

Filters: `titleInclude`, `titleExclude`, `countries` (ISO codes such as `FR`, `US`), `cities`, `departments`,
`remoteOnly`, `maxJobsPerCompany`. Options: `mode` (`snapshot` / `changes`), `stateKey`, `history90d`,
`includeDescriptionExcerpt`, `dedupeMultiLocation`.

## `changes` mode

With `"mode": "changes"` and a `stateKey`, each run returns only jobs that are new, changed, reopened or closed since
**your previous run with the same `stateKey`** (the baseline is stored in a key-value store of your own Apify
account). The first run with a new `stateKey` has no baseline and returns the full list, so cap it with
`maxJobsPerCompany` or filters.

## Output

Rows have a `type`: `job`, `company` (summary and trends) or `coverage` (free, one per requested company).
Trend fields (`netChange7d`, ...) stay `null` until enough history is collected (history started 15 November 2026).
