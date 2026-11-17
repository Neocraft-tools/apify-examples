"""Capture web pages with neocraft/website-screenshot-pro and download the files.

Usage:
    export APIFY_TOKEN="<your-apify-token>"
    pip install -r requirements.txt
    python screenshot.py https://example.com https://apify.com

Cost: $0.008 per saved capture (URLs x devices). The run is capped with max_total_charge_usd.
"""
import os
import sys
import urllib.request
from decimal import Decimal
from pathlib import Path

from apify_client import ApifyClient

ACTOR_ID = "neocraft/website-screenshot-pro"
DEVICES = ["desktop", "mobile"]
OUT = Path("screenshots")


def main() -> int:
    urls = sys.argv[1:] or ["https://example.com"]
    client = ApifyClient(os.environ["APIFY_TOKEN"])

    run_input = {
        "urls": urls,
        "devices": DEVICES,
        "format": "png",
        "captureMode": "fullPage",
        "maxHeight": 8000,
        "cookieBanners": "hide",   # hidden with CSS, nothing is clicked, no consent given
        "blockAds": True,
    }
    captures = len(urls) * len(DEVICES)
    run = client.actor(ACTOR_ID).call(
        run_input=run_input,
        max_total_charge_usd=Decimal("0.008") * captures + Decimal("0.01"),
    )
    if run is None or run.status != "SUCCEEDED":
        print(f"Run did not succeed: {run.status if run else 'no run'}", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)
    for row in client.dataset(run.default_dataset_id).iterate_items():
        if row["status"] != "ok":
            print(f"{row['url']} [{row.get('device')}]: {row['status']} {row.get('errorCode')} - {row.get('errorMessage')}")
            continue
        target = OUT / row["screenshotKey"]
        urllib.request.urlretrieve(row["screenshotUrl"], target)
        note = " (truncated at maxHeight)" if row.get("truncated") else ""
        print(f"{row['url']} [{row['device']}]: {row['width']}x{row['height']} -> {target}{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
