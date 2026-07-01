#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Stop Script
# Gracefully stops all Agent X PM2 processes.
# Usage:
#   bash termux/stop.sh            # stop all
#   bash termux/stop.sh core       # stop agent-x-core only
#   bash termux/stop.sh twin
#   bash termux/stop.sh dashboard
#   bash termux/stop.sh webhook
#   bash termux/stop.sh kill       # force-kill + delete all PM2 entries
# =============================================================================

set -euo pipefail

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

log()  { echo -e "${GREEN}[stop]${RESET} $*"; }
warn() { echo -e "${YELLOW}[warn]${RESET}  $*"; }

TARGET="${1:-all}"

pm2_stop() {
  local name="$1"
  pm2 stop "${name}" 2>/dev/null && log "Stopped ${name}" || warn "${name} was not running"
}

case "${TARGET}" in
  core)      pm2_stop "agent-x-core" ;;
  twin)      pm2_stop "digital-twin" ;;
  dashboard) pm2_stop "dashboard" ;;
  webhook)   pm2_stop "webhook-listener" ;;
  kill)
    log "Force-killing and deleting all PM2 agent-x processes…"
    for svc in agent-x-core digital-twin dashboard webhook-listener; do
      pm2 delete "${svc}" 2>/dev/null || true
    done
    pm2 save --force
    log "All processes removed from PM2."
    ;;
  all)
    pm2_stop "agent-x-core"
    pm2_stop "digital-twin"
    pm2_stop "dashboard"
    pm2_stop "webhook-listener"
    pm2 save --force
    log "All services stopped."
    ;;
  *)
    echo "Usage: bash termux/stop.sh [all|core|twin|dashboard|webhook|kill]"
    exit 1
    ;;
esac

pm2 list
