"""Audit one or more websites with neocraft/website-audit-all-in-one and print the essentials.

Usage:
    export APIFY_TOKEN="<your-apify-token>"
    pip install -r requirements.txt
    python audit.py https://example.com https://www.example.org

Cost: $0.49 per site with maxPagesPerSite=10 (the run is capped with max_total_charge_usd).
"""
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "neocraft/website-audit-all-in-one"


def main() -> int:
    urls = sys.argv[1:] or ["https://example.com"]
    client = ApifyClient(os.environ["APIFY_TOKEN"])

    run_input = {
        "startUrls": [{"url": u} for u in urls],
        "maxPagesPerSite": 10,      # first 10 pages are included in the $0.49
        "language": "en",
        "pageRecords": False,       # only the site-level items, not one item per page
        "monitorId": "examples",    # keeps a separate history, enables changes.scoreDelta on the next run
    }

    # call() starts the run and waits for it to finish.
    run = client.actor(ACTOR_ID).call(
        run_input=run_input,
        max_total_charge_usd=Decimal("0.49") * len(urls) + Decimal("0.10"),
    )
    if run is None or run.status != "SUCCEEDED":
        print(f"Run did not succeed: {run.status if run else 'no run'}", file=sys.stderr)
        return 1

    items = client.dataset(run.default_dataset_id).iterate_items()
    for item in items:
        if item.get("type", "site") != "site":
            continue
        s = item["summary"]
        geo = (item.get("scores") or {}).get("categories", {}).get("geo")
        print(f"\n{item['finalUrl']}: {s['score']}/100 (grade {s['grade']}), AI visibility (GEO): {geo}")
        print(f"  {s['headline']}")
        print(f"  critical={s['critical']} high={s['high']} medium={s['medium']} low={s['low']}")
        for p in item.get("topPriorities", []):
            print(f"  #{p['rank']} [{p['severity']}] {p['title']}\n      first step: {p['firstStep']}")
        delta = (item.get("changes") or {}).get("scoreDelta")
        if delta is not None:
            print(f"  score change since previous audit: {delta:+d}")

    print(f"\nHTML report: https://api.apify.com/v2/key-value-stores/{run.default_key_value_store_id}/records/OUTPUT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
