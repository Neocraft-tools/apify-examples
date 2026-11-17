#!/usr/bin/env bash
# One synchronous call to neocraft/website-screenshot-pro; prints the public image URL of each capture.
#
# Usage: APIFY_TOKEN=... bash run-sync.sh https://example.com [device]
# Needs: curl, jq. Cost: $0.008 per capture.
set -euo pipefail

URL="${1:-https://example.com}"
DEVICE="${2:-laptop}"

curl -sS --fail-with-body -X POST \
  "https://api.apify.com/v2/acts/neocraft~website-screenshot-pro/run-sync-get-dataset-items?maxTotalChargeUsd=0.05" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg url "$URL" --arg dev "$DEVICE" \
        '{urls: [$url], devices: [$dev], captureMode: "viewport", format: "jpeg", quality: 70}')" \
  | jq -r '.[] | if .status == "ok" then .screenshotUrl else "\(.url): \(.errorCode) \(.errorMessage)" end'
