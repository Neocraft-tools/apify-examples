# Company hiring tracker from an AI agent (MCP)

Apify hosts an MCP server at `https://mcp.apify.com`. To give an agent **only this Actor** (plus the helper tools it
needs to read results), select it with the `tools` parameter:

```
https://mcp.apify.com?tools=neocraft/company-hiring-tracker
```

## Remote server (recommended: OAuth, no token in the config)

```json
{
  "mcpServers": {
    "apify": { "url": "https://mcp.apify.com?tools=neocraft/company-hiring-tracker" }
  }
}
```

On first connection the client opens a browser window to sign in to Apify. Clients that cannot do OAuth can send an
`Authorization: Bearer <APIFY_TOKEN>` header instead (keep the token out of repositories).

## Local server (stdio, Node.js 22+)

```json
{
  "mcpServers": {
    "apify-local": {
      "command": "npx",
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "neocraft/company-hiring-tracker"],
      "env": { "APIFY_TOKEN": "<your-apify-token>" }
    }
  }
}
```

Docs: <https://docs.apify.com/platform/integrations/mcp> · configurator: <https://mcp.apify.com>

## Prompt example

> With the hiring tracker, check Stripe, doctolib.fr and https://boards.greenhouse.io/airbnb (maxJobsPerCompany 20, countries FR and US). Summarise who is hiring the most engineers and whether hiring is accelerating.

## What the agent should read

One dataset, three row types (`type`):

* `company`: `openJobs`, `netChange7d` / `netChange30d` / `netChange90d`, `byDepartment`, `byCountry`, and a one-sentence `summary` (rule-based, no AI). Read these first.
* `job`: `company`, `title`, `department`, `locations`, `country`, `remote`, `postedAt`, `firstSeenAt`, `daysOpen`, `url`; in `changes` mode also `changeType` (`new`, `changed`, `reopened`, `closed`).
* `coverage` (free): whether each requested company was found, its job board, and the `reason` when it is not covered.

Trend fields are `null` until enough history exists (collection started on 15 November 2026).

Cost: $0.004 per covered company + $0.001 per returned job. Use `maxJobsPerCompany` to cap big employers.
