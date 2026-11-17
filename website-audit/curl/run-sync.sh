#!/usr/bin/env bash
# One synchronous call to neocraft/website-audit-all-in-one, then a pass/fail gate with jq.
#
# Usage: APIFY_TOKEN=... bash run-sync.sh https://staging.example.com [min_score]
# Needs: curl, jq. Cost: $0.49 (10 pages).
#
# run-sync-get-dataset-items holds the HTTP request open for at most 300 s, so keep the audit small
# (10 pages, pageRecords off, PageSpeed off). For bigger audits use the Python/Node examples.
set -euo pipefail

URL="${1:-https://example.com}"
MIN_SCORE="${2:-70}"

curl -sS --fail-with-body -X POST \
  "https://api.apify.com/v2/acts/neocraft~website-audit-all-in-one/run-sync-get-dataset-items?maxTotalChargeUsd=0.6" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"startUrls\":[{\"url\":\"${URL}\"}],\"maxPagesPerSite\":10,\"pageRecords\":false,\"pagespeed\":false,\"monitorId\":\"ci\"}" \
  > audit.json

SITE='[.[] | select((.type // "site") == "site")][0]'
SCORE=$(jq "${SITE}.summary.score" audit.json)
CRIT=$(jq "${SITE}.summary.critical" audit.json)
DELTA=$(jq "${SITE}.changes.scoreDelta // 0" audit.json)
GEO=$(jq "${SITE}.scores.categories.geo" audit.json)

echo "score=${SCORE} critical=${CRIT} delta=${DELTA} geo=${GEO}"
jq -r "${SITE}.topPriorities[] | \"#\\(.rank) [\\(.severity)] \\(.title) -> \\(.firstStep)\"" audit.json

if [ "${SCORE}" -lt "${MIN_SCORE}" ] || [ "${CRIT}" -gt 0 ] || [ "${DELTA}" -le -5 ]; then
  echo "Website audit gate failed" >&2
  exit 1
fi
