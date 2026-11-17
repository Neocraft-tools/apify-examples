// Audit one or more websites with neocraft/website-audit-all-in-one and print the essentials.
//
// Usage:
//   export APIFY_TOKEN="<your-apify-token>"
//   npm install
//   node audit.mjs https://example.com https://www.example.org
//
// Cost: $0.49 per site with maxPagesPerSite=10 (capped with maxTotalChargeUsd).
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'neocraft/website-audit-all-in-one';
const urls = process.argv.slice(2).length ? process.argv.slice(2) : ['https://example.com'];

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const input = {
    startUrls: urls.map((url) => ({ url })),
    maxPagesPerSite: 10, // first 10 pages are included in the $0.49
    language: 'en',
    pageRecords: false, // only the site-level items
    monitorId: 'examples', // separate history; enables changes.scoreDelta on the next run
};

// call() starts the run and waits for it to finish.
const run = await client.actor(ACTOR_ID).call(input, {
    maxTotalChargeUsd: 0.49 * urls.length + 0.1,
});
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status}`);
    process.exit(1);
}

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items.filter((i) => (i.type ?? 'site') === 'site')) {
    const s = item.summary;
    console.log(`\n${item.finalUrl}: ${s.score}/100 (grade ${s.grade}), AI visibility (GEO): ${item.scores?.categories?.geo}`);
    console.log(`  ${s.headline}`);
    console.log(`  critical=${s.critical} high=${s.high} medium=${s.medium} low=${s.low}`);
    for (const p of item.topPriorities ?? []) {
        console.log(`  #${p.rank} [${p.severity}] ${p.title}\n      first step: ${p.firstStep}`);
    }
    if (item.changes?.scoreDelta != null) console.log(`  score change since previous audit: ${item.changes.scoreDelta}`);
}

console.log(`\nHTML report: https://api.apify.com/v2/key-value-stores/${run.defaultKeyValueStoreId}/records/OUTPUT`);
