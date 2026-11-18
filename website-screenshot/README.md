# Website Screenshot Pro: examples

Actor: [`neocraft/website-screenshot-pro`](https://apify.com/neocraft/website-screenshot-pro) ·
$0.008 per saved capture (image or PDF); refused, duplicate and skipped URLs are free; the first 20 failed attempts
of a run are free, then $0.0005 each.

| Example | File |
|---|---|
| Python: capture URLs on several devices and download the files | [`python/screenshot.py`](python/screenshot.py) |
| Node.js: same | [`node/screenshot.mjs`](node/screenshot.mjs) |
| curl + jq: one synchronous call, print the image URL | [`curl/run-sync.sh`](curl/run-sync.sh) |
| GitHub Actions: weekly full-page capture of competitors' pricing pages, kept as a build artifact | [`github-actions/weekly-competitor-pricing.yml`](github-actions/weekly-competitor-pricing.yml) |
| AI agents / MCP | [`ai-agents-mcp.md`](ai-agents-mcp.md) |

## Output

One dataset row per URL x device: `url`, `inputIndex`, `status` (`ok` / `error` / `skipped`), `errorCode`,
`errorMessage`, `device`, `format`, `captureMode`, `screenshotUrl`, `screenshotKey`, `contentType`, `bytes`,
`width`, `height`, `truncated`. Files are stored in the run's default key-value store and kept for your Apify
plan's data-retention period, so download what you want to keep.

## Useful input fields

`urls` (required), `devices` (`desktop`, `desktop-hd`, `laptop`, `laptop-small`, `tablet`, `tablet-landscape`,
`mobile`, `mobile-small`, `mobile-android`, `custom`), `format` (`png` / `jpeg` / `webp` / `pdf`), `quality`,
`captureMode` (`fullPage` / `viewport` / `element` / `clip`), `elementSelector`, `maxHeight`, `waitUntil`,
`delayMs`, `waitForSelector`, `cookieBanners` (`hide` / `reject` / `accept` / `none`), `blockAds`,
`hideSelectors`, `colorScheme`, `locale`. Full list on the Actor's **Input** tab.

## GitHub Action

The same call is packaged as a reusable action: [`Neocraft-tools/website-screenshot-action@v1`](https://github.com/Neocraft-tools/website-screenshot-action).
