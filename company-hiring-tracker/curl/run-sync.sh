#!/usr/bin/env bash
# Weekly-style check in one synchronous call: only jobs that are new / changed / reopened / closed
# since your previous run with the same stateKey (the first run returns everything = baseline).
#
# Usage: APIFY_TOKEN=... bash run-sync.sh
# Needs: curl, jq. Cost: $0.004 per covered company + $0.001 per returned job (capped at $0.50 here).
set -euo pipefail

curl -sS --fail-with-body -X POST \
  "https://api.apify.com/v2/acts/neocraft~company-hiring-tracker/run-sync-get-dataset-items?maxTotalChargeUsd=0.5" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"companies":["stripe.com","doctolib.fr"],"mode":"changes","stateKey":"my-accounts","titleInclude":["engineer"],"maxJobsPerCompany":50}' \
  > hiring.json

jq -r '.[] | select(.type == "job") | "\(.changeType)\t\(.company)\t\(.title)\t\(.url)"' hiring.json
jq -r '.[] | select(.type == "company") | "\(.company): \(.summary)"' hiring.json
