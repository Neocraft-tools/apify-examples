# Website audit from an AI agent (MCP)

Apify hosts an MCP server at `https://mcp.apify.com`. To give an agent **only this Actor** (plus the helper tools it
needs to read results), select it with the `tools` parameter:

```
https://mcp.apify.com?tools=neocraft/website-audit-all-in-one
```

## Remote server (recommended: OAuth, no token in the config)

```json
{
  "mcpServers": {
    "apify": { "url": "https://mcp.apify.com?tools=neocraft/website-audit-all-in-one" }
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
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "neocraft/website-audit-all-in-one"],
      "env": { "APIFY_TOKEN": "<your-apify-token>" }
    }
  }
}
```

Docs: <https://docs.apify.com/platform/integrations/mcp> · configurator: <https://mcp.apify.com>

## Prompt example

> Audit https://example.com with the website audit tool (maxPagesPerSite 10, pageRecords false). Tell me whether ChatGPT, Claude and Perplexity crawlers may read the site, then list the 3 quick wins with their first step.

## What the agent should read

The `site` item is large. Point the agent to the compact fields first:

* `summary` (score, grade, counts per severity, one-sentence `headline`)
* `topPriorities[]` and `quickWins[]` (title, severity, `firstStep`, `whoCanFix`)
* `scores.categories.geo` and `scores.breakdown.geo` (AI-visibility pillars)
* `findings[]` filtered on `category == "geo"` for the AI-crawler details

Each audit costs $0.49 (10 pages). Set a maximum charge per run in your Apify account so an agent cannot overspend.
