#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Status Script
# Shows PM2 process table + quick health-check pings for each service.
# =============================================================================

set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Load env for port numbers
if [[ -f "${ENV_FILE}" ]]; then
  set -a; source "${ENV_FILE}"; set +a
fi

CORE_PORT="${PORT:-3000}"
TWIN_PORT="${DIGITAL_TWIN_PORT:-3002}"
DASH_PORT="${DASHBOARD_PORT:-5000}"

echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${RESET}"
echo -e "${BOLD}${CYAN}         Agent X — Termux Status           ${RESET}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${RESET}"
echo ""

# --------------------------------------------------------------------------- #
# PM2 process list
# --------------------------------------------------------------------------- #
echo -e "${BOLD}PM2 Processes:${RESET}"
pm2 list 2>/dev/null || echo "  PM2 not running or no processes registered."
echo ""

# --------------------------------------------------------------------------- #
# HTTP health checks
# --------------------------------------------------------------------------- #
http_check() {
  local label="$1"
  local url="$2"
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "${url}" 2>/dev/null || echo "000")
  if [[ "${code}" == "200" || "${code}" == "204" ]]; then
    echo -e "  ${GREEN}✔${RESET} ${label} — ${url}  [HTTP ${code}]"
  else
    echo -e "  ${RED}✘${RESET} ${label} — ${url}  [HTTP ${code}]"
  fi
}

echo -e "${BOLD}HTTP Health Checks:${RESET}"
http_check "agent-x-core     " "http://localhost:${CORE_PORT}/health"
http_check "digital-twin     " "http://localhost:${TWIN_PORT}/health"
http_check "dashboard        " "http://localhost:${DASH_PORT}/"
echo ""

# --------------------------------------------------------------------------- #
# Memory / state files
# --------------------------------------------------------------------------- #
echo -e "${BOLD}State Files:${RESET}"
for f in \
  "${REPO_DIR}/memory/state.json" \
  "${REPO_DIR}/memory/tasks.json" \
  "${REPO_DIR}/data/db.json" \
  "${REPO_DIR}/data/revenue.json"; do
  if [[ -f "${f}" ]]; then
    size=$(wc -c < "${f}" 2>/dev/null || echo "?")
    echo -e "  ${GREEN}✔${RESET}  ${f}  (${size} bytes)"
  else
    echo -e "  ${YELLOW}–${RESET}  ${f}  (missing)"
  fi
done
echo ""

# --------------------------------------------------------------------------- #
# Log tail (last 5 lines each)
# --------------------------------------------------------------------------- #
echo -e "${BOLD}Recent Logs (last 5 lines):${RESET}"
for svc in agent-x-core digital-twin dashboard webhook-listener; do
  log_file="${REPO_DIR}/logs/${svc}.log"
  if [[ -f "${log_file}" ]]; then
    echo -e "  ${CYAN}--- ${svc} ---${RESET}"
    tail -n 5 "${log_file}" | sed 's/^/    /'
  fi
done
echo ""
