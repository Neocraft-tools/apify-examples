// Capture web pages with neocraft/website-screenshot-pro and download the files.
//
// Usage:
//   export APIFY_TOKEN="<your-apify-token>"
//   npm install
//   node screenshot.mjs https://example.com https://apify.com
//
// Cost: $0.008 per saved capture (URLs x devices), capped with maxTotalChargeUsd.
import { mkdir, writeFile } from 'node:fs/promises';
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'neocraft/website-screenshot-pro';
const DEVICES = ['desktop', 'mobile'];
const urls = process.argv.slice(2).length ? process.argv.slice(2) : ['https://example.com'];

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor(ACTOR_ID).call(
    {
        urls,
        devices: DEVICES,
        format: 'png',
        captureMode: 'fullPage',
        maxHeight: 8000,
        cookieBanners: 'hide',
        blockAds: true,
    },
    { maxTotalChargeUsd: 0.008 * urls.length * DEVICES.length + 0.01 },
);
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status}`);
    process.exit(1);
}

await mkdir('screenshots', { recursive: true });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const row of items) {
    if (row.status !== 'ok') {
        console.log(`${row.url} [${row.device}]: ${row.status} ${row.errorCode} - ${row.errorMessage}`);
        continue;
    }
    const res = await fetch(row.screenshotUrl); // Node 18+ has fetch built in
    const file = `screenshots/${row.screenshotKey}`;
    await writeFile(file, Buffer.from(await res.arrayBuffer()));
    console.log(`${row.url} [${row.device}]: ${row.width}x${row.height} -> ${file}${row.truncated ? ' (truncated)' : ''}`);
}
