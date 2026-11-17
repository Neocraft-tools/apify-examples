# Website screenshots from an AI agent (MCP)

Apify hosts an MCP server at `https://mcp.apify.com`. To give an agent **only this Actor** (plus the helper tools it
needs to read results), select it with the `tools` parameter:

```
https://mcp.apify.com?tools=neocraft/website-screenshot-pro
```

## Remote server (recommended: OAuth, no token in the config)

```json
{
  "mcpServers": {
    "apify": { "url": "https://mcp.apify.com?tools=neocraft/website-screenshot-pro" }
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
      "args": ["-y", "@apify/actors-mcp-server", "--tools", "neocraft/website-screenshot-pro"],
      "env": { "APIFY_TOKEN": "<your-apify-token>" }
    }
  }
}
```

Docs: <https://docs.apify.com/platform/integrations/mcp> · configurator: <https://mcp.apify.com>

## Prompt example

> Take a viewport screenshot of https://example.com on the `mobile` device as JPEG quality 70, open the image from `screenshotUrl` and tell me if anything in the header overlaps or is cut off.

## What the agent should read

Each dataset row is one capture:

* `status` (`ok` / `error` / `skipped`) and, on failure, `errorCode` (`DNS_ERROR`, `TIMEOUT`, `BLOCKED_BY_SITE`, ...) and `errorMessage`
* `screenshotUrl`: direct link to the file in the run's key-value store, readable by a vision model
* `device`, `width`, `height`, `truncated`

Viewport JPEGs (quality 60-80) keep images small for vision models; use `fullPage` with `maxHeight` when the whole page matters.

Each saved capture costs $0.008. Note that `screenshotUrl` is readable by anyone who has the link.
