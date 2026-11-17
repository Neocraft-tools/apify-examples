# Neocraft Apify examples

Runnable examples (Python, Node.js, curl, GitHub Actions, AI agents / MCP) for three pay-per-event
[Apify](https://apify.com) Actors published by **Neocraft**:

| Actor | What it does | Price (pay per event, platform usage included) |
|---|---|---|
| [Website Audit All-in-One](https://apify.com/neocraft/website-audit-all-in-one) | AI search visibility (GEO: can ChatGPT, Claude, Perplexity read your site?), page-by-page SEO, security headers/SSL, e-mail DNS (SPF/DMARC), WordPress/CMS known vulnerabilities, speed, accessibility. Score 0-100, prioritized fixes, HTML/PDF report, change tracking between runs. | **$0.49 per site** (first 10 pages included), $0.01 per extra page. Unreachable sites are not charged. |
| [Website Screenshot Pro](https://apify.com/neocraft/website-screenshot-pro) | Full-page / viewport / element / clip screenshots and PDFs in PNG, JPEG, WebP or PDF, 10 device presets, cookie-banner hiding, ad blocking. | **$0.008 per saved capture** ($8 / 1,000). The first 20 failed attempts of a run are free, then $0.0005 each. |
| [Company Hiring Tracker](https://apify.com/neocraft/company-hiring-tracker) | Open jobs of companies from their public job boards (Greenhouse, Lever, Ashby, Workable, ...), with trends (net change 7/30/90 days) and a `changes` mode that returns only new / changed / reopened / closed jobs since your previous run. | **$0.004 per covered company** + **$0.001 per returned job**; optional 90-day history $0.02 per company. Companies not covered are free. |

Prices are those listed on the Apify Store pages at the time of writing; the Store page is the reference.
All three Actors accept a *maximum total charge* per run, and every example here sets one.

## Repository layout

```
website-audit/            # neocraft/website-audit-all-in-one
website-screenshot/       # neocraft/website-screenshot-pro
company-hiring-tracker/   # neocraft/company-hiring-tracker
  python/                 # apify-client (Python) script + requirements.txt
  node/                   # apify-client (Node.js) script + package.json
  curl/                   # one synchronous HTTP call (run-sync-get-dataset-items)
  github-actions/         # workflow to copy into .github/workflows/ of YOUR repo
  ai-agents-mcp.md        # use the Actor as a tool from Claude, Cursor or any MCP client
```

The workflows are kept outside `.github/workflows/` on purpose, so they do not run in this repository.

## Setup

1. Create a free Apify account and copy your API token from **Console > Settings > API & Integrations**.
2. Export it (never commit it):

   ```bash
   export APIFY_TOKEN="<your-apify-token>"
   ```

3. Pick an example:

   ```bash
   # Python 3.10+
   cd website-audit/python && pip install -r requirements.txt && python audit.py https://example.com
   # Node.js 18+
   cd website-audit/node && npm install && node audit.mjs https://example.com
   # curl + jq
   bash website-audit/curl/run-sync.sh https://example.com
   ```

## Two ways to call an Actor

* **Client libraries** (`apify-client` for Python and Node.js): `actor(...).call(...)` starts a run, waits for it to
  finish, and returns the run object; the results are then read from the run's default dataset. Use this for
  anything that may take more than a few minutes.
* **`run-sync-get-dataset-items`** endpoint: one `POST` that starts the run, waits, and returns the dataset items as
  JSON. The HTTP request is held open for at most **300 seconds**; if the run takes longer, you get a timeout
  response (HTTP 408) while the run keeps going in your account. Keep these calls small.

API reference: <https://docs.apify.com/api/v2> · Python client: <https://docs.apify.com/api/client/python> ·
JavaScript client: <https://docs.apify.com/api/client/js>

## About

Maintained by **Xiaoli, an AI assistant, for Neocraft**; reviewed by a human before publication.
Issues and suggestions are welcome. Released under the [MIT license](LICENSE).

The Actors only read public pages and public job boards. Audit websites and capture pages you are allowed to
access, and respect the sites' terms of use.
