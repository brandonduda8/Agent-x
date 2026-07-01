#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Log Viewer
# Usage:
#   bash termux/logs.sh              # tail all logs via pm2
#   bash termux/logs.sh core         # tail agent-x-core only
#   bash termux/logs.sh twin
#   bash termux/logs.sh dashboard
#   bash termux/logs.sh webhook
#   bash termux/logs.sh file <name>  # tail raw log file
# =============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-all}"

case "${TARGET}" in
  core)     pm2 logs agent-x-core --lines 50 ;;
  twin)     pm2 logs digital-twin --lines 50 ;;
  dashboard) pm2 logs dashboard --lines 50 ;;
  webhook)  pm2 logs webhook-listener --lines 50 ;;
  file)
    log_file="${REPO_DIR}/logs/${2:-agent-x-core}.log"
    [[ -f "${log_file}" ]] && tail -f "${log_file}" || echo "Log not found: ${log_file}"
    ;;
  all)      pm2 logs --lines 50 ;;
  *)
    echo "Usage: bash termux/logs.sh [all|core|twin|dashboard|webhook|file <name>]"
    ;;
esac
