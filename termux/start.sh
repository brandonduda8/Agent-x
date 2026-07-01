#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Start Script
# Launches all Agent X services via PM2 (replaces systemd).
# Usage:
#   bash termux/start.sh            # start all services
#   bash termux/start.sh core       # start agent-x-core only
#   bash termux/start.sh twin       # start digital-twin only
#   bash termux/start.sh dashboard  # start Python dashboard only
#   bash termux/start.sh webhook    # start webhook-listener only
# =============================================================================

set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

log()  { echo -e "${GREEN}[start]${RESET} $*"; }
warn() { echo -e "${YELLOW}[warn]${RESET}  $*"; }
fail() { echo -e "${RED}[fail]${RESET}  $*"; exit 1; }

# --------------------------------------------------------------------------- #
# Guards
# --------------------------------------------------------------------------- #
[[ -f "${ENV_FILE}" ]] || fail ".env not found. Run: bash termux/setup.sh"
command -v node  >/dev/null 2>&1 || fail "node not found. Run: pkg install nodejs"
command -v pm2   >/dev/null 2>&1 || fail "pm2 not found. Run: npm install -g pm2"
command -v python >/dev/null 2>&1 || fail "python not found. Run: pkg install python"

# Load env so PORT vars are available for display
set -a; source "${ENV_FILE}"; set +a

CORE_PORT="${PORT:-3000}"
TWIN_PORT="${DIGITAL_TWIN_PORT:-3002}"
DASH_PORT="${DASHBOARD_PORT:-5000}"

# --------------------------------------------------------------------------- #
# Service definitions
# --------------------------------------------------------------------------- #
start_core() {
  log "Starting agent-x-core on port ${CORE_PORT}…"
  pm2 start "${REPO_DIR}/agent-x-core/index.js" \
    --name "agent-x-core" \
    --env production \
    --env-file "${ENV_FILE}" \
    --cwd "${REPO_DIR}/agent-x-core" \
    --log "${REPO_DIR}/logs/agent-x-core.log" \
    --time \
    -- 2>/dev/null || pm2 restart agent-x-core 2>/dev/null || true
}

start_twin() {
  log "Starting digital-twin on port ${TWIN_PORT}…"
  pm2 start "${REPO_DIR}/digital-twin/index.js" \
    --name "digital-twin" \
    --env production \
    --env-file "${ENV_FILE}" \
    --cwd "${REPO_DIR}/digital-twin" \
    --log "${REPO_DIR}/logs/digital-twin.log" \
    --time \
    -- 2>/dev/null || pm2 restart digital-twin 2>/dev/null || true
}

start_dashboard() {
  log "Starting Python dashboard on port ${DASH_PORT}…"
  pm2 start "${REPO_DIR}/termux/run_dashboard.sh" \
    --name "dashboard" \
    --interpreter bash \
    --cwd "${REPO_DIR}/dashboard" \
    --log "${REPO_DIR}/logs/dashboard.log" \
    --time \
    -- 2>/dev/null || pm2 restart dashboard 2>/dev/null || true
}

start_webhook() {
  log "Starting webhook-listener…"
  pm2 start "${REPO_DIR}/webhook-listener/index.js" \
    --name "webhook-listener" \
    --env production \
    --env-file "${ENV_FILE}" \
    --cwd "${REPO_DIR}/webhook-listener" \
    --log "${REPO_DIR}/logs/webhook-listener.log" \
    --time \
    -- 2>/dev/null || pm2 restart webhook-listener 2>/dev/null || true
}

# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #
TARGET="${1:-all}"

case "${TARGET}" in
  core)       start_core ;;
  twin)       start_twin ;;
  dashboard)  start_dashboard ;;
  webhook)    start_webhook ;;
  all)
    start_core
    start_twin
    start_dashboard
    start_webhook
    ;;
  *)
    fail "Unknown target '${TARGET}'. Valid: all | core | twin | dashboard | webhook"
    ;;
esac

# --------------------------------------------------------------------------- #
# Save PM2 process list so termux-boot can restore it
# --------------------------------------------------------------------------- #
pm2 save --force

log "All requested services started."
echo ""
pm2 list
echo ""
echo "  Logs:    pm2 logs"
echo "  Status:  bash termux/status.sh"
echo "  Stop:    bash termux/stop.sh"
