// Track open jobs of a few companies with neocraft/company-hiring-tracker.
//
// Usage:
//   export APIFY_TOKEN="<your-apify-token>"
//   npm install
//   node hiring.mjs
//
// Cost: $0.004 per covered company + $0.001 per returned job (capped with maxTotalChargeUsd).
import { ApifyClient } from 'apify-client';

const ACTOR_ID = 'neocraft/company-hiring-tracker';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor(ACTOR_ID).call(
    {
        companies: ['Stripe', { name: 'Doctolib', domain: 'doctolib.fr' }, 'https://boards.greenhouse.io/airbnb'],
        titleInclude: ['engineer', 'data'],
        countries: ['FR', 'US'],
        maxJobsPerCompany: 20,
        mode: 'snapshot', // use 'changes' + a stateKey for weekly monitoring
    },
    { maxTotalChargeUsd: 0.1 },
);
if (run.status !== 'SUCCEEDED') {
    console.error(`Run did not succeed: ${run.status}`);
    process.exit(1);
}

const { items } = await client.dataset(run.defaultDatasetId).listItems();
const byType = (t) => items.filter((i) => i.type === t);

for (const c of byType('coverage').filter((c) => !c.covered)) {
    console.log(`Not covered (free): ${c.query} - ${c.reason}`);
}
for (const c of byType('company')) {
    console.log(`\n== ${c.company}: ${c.openJobs} open jobs (30-day net change: ${c.netChange30d})`);
    console.log(`   ${c.summary}`);
    for (const j of byType('job').filter((j) => j.company === c.company).slice(0, 5)) {
        console.log(`   - ${j.title} | ${j.locations} | ${j.url}`);
    }
}
