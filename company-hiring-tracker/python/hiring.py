"""Track open jobs of a few companies with neocraft/company-hiring-tracker.

Usage:
    export APIFY_TOKEN="<your-apify-token>"
    pip install -r requirements.txt
    python hiring.py

Cost: $0.004 per covered company + $0.001 per returned job (here at most 3 x 0.004 + 60 x 0.001 = $0.072).
"""
import os
import sys
from collections import defaultdict
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "neocraft/company-hiring-tracker"


def main() -> int:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run_input = {
        "companies": [
            "Stripe",
            {"name": "Doctolib", "domain": "doctolib.fr"},
            "https://boards.greenhouse.io/airbnb",
        ],
        "titleInclude": ["engineer", "data"],
        "countries": ["FR", "US"],
        "maxJobsPerCompany": 20,   # most recent first; caps the cost of big employers
        "mode": "snapshot",        # use "changes" + a stateKey for weekly monitoring
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=Decimal("0.10"))
    if run is None or run.status != "SUCCEEDED":
        print(f"Run did not succeed: {run.status if run else 'no run'}", file=sys.stderr)
        return 1

    rows = defaultdict(list)
    for item in client.dataset(run.default_dataset_id).iterate_items():
        rows[item.get("type")].append(item)

    for c in rows["coverage"]:
        if not c.get("covered"):
            print(f"Not covered (free): {c.get('query')} - {c.get('reason')}")

    for c in rows["company"]:
        print(f"\n== {c['company']}: {c.get('openJobs')} open jobs (30-day net change: {c.get('netChange30d')})")
        print(f"   {c.get('summary')}")
        for j in [j for j in rows["job"] if j.get("company") == c["company"]][:5]:
            print(f"   - {j.get('title')} | {j.get('locations')} | {j.get('url')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
