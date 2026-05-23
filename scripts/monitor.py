#!/bin/bash
# =============================================================================
# monitor.sh — Application Health Monitor
# Usage: bash scripts/monitor.sh [APP_URL] [CHECK_INTERVAL_SECONDS]
#
# What it does:
#   - Pings the /health endpoint every N seconds
#   - Logs status with timestamp
#   - Alerts if app goes down (can be extended with email/Slack notifications)
# =============================================================================

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
APP_URL="${1:-http://localhost:5000}"
INTERVAL="${2:-30}"
LOG_FILE="logs/monitor.log"
HEALTH_ENDPOINT="${APP_URL}/health"

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'   # No Color

# ── Helpers ───────────────────────────────────────────────────────────────────
timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

log() {
  local level="$1"
  local message="$2"
  echo "[$(timestamp)] [$level] $message" | tee -a "$LOG_FILE"
}

# ── Setup ─────────────────────────────────────────────────────────────────────
mkdir -p logs
echo "=============================================" | tee -a "$LOG_FILE"
log "INFO" "Starting monitor for: $HEALTH_ENDPOINT"
log "INFO" "Check interval: ${INTERVAL}s"
echo "=============================================" | tee -a "$LOG_FILE"

# ── Monitor Loop ──────────────────────────────────────────────────────────────
FAIL_COUNT=0
MAX_FAILURES=3

while true; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$HEALTH_ENDPOINT" || echo "000")

  if [ "$HTTP_STATUS" -eq 200 ]; then
    echo -e "${GREEN}[$(timestamp)] ✅ HEALTHY — HTTP $HTTP_STATUS${NC}" | tee -a "$LOG_FILE"
    FAIL_COUNT=0
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo -e "${RED}[$(timestamp)] ❌ UNHEALTHY — HTTP $HTTP_STATUS (Failure $FAIL_COUNT/$MAX_FAILURES)${NC}" | tee -a "$LOG_FILE"

    if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
      echo -e "${YELLOW}[$(timestamp)] 🚨 ALERT: App has been down for $FAIL_COUNT consecutive checks!${NC}" | tee -a "$LOG_FILE"
      # Extend here: send email, post to Slack webhook, trigger PagerDuty, etc.
      # Example Slack webhook (add your URL to environment):
      # curl -X POST -H 'Content-type: application/json' \
      #   --data "{\"text\":\"🚨 App DOWN at $HEALTH_ENDPOINT\"}" \
      #   "$SLACK_WEBHOOK_URL"
    fi
  fi

  sleep "$INTERVAL"
done
