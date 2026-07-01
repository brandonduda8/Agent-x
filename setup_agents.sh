#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Agent Setup Script (Termux-compatible)
# Sets up agent directories, installs per-agent dependencies, validates configs.
#
# Previously contained hardcoded /usr/local/bin paths and systemd commands —
# all replaced with $PREFIX-relative paths and PM2.
# =============================================================================

set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${REPO_DIR}/.env"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BOLD="\033[1m"
RESET="\033[0m"

log()  { echo -e "${GREEN}[agents]${RESET} $*"; }
warn() { echo -e "${YELLOW}[warn]${RESET}   $*"; }
fail() { echo -e "${RED}[fail]${RESET}   $*"; exit 1; }

log "Agent X — Agent Setup"
log "Repo: ${REPO_DIR}"

# --------------------------------------------------------------------------- #
# Load .env if available
# --------------------------------------------------------------------------- #
if [[ -f "${ENV_FILE}" ]]; then
  set -a; source "${ENV_FILE}"; set +a
  log "Loaded .env"
else
  warn ".env not found — using defaults. Run termux/setup.sh first."
fi

# --------------------------------------------------------------------------- #
# Validate Node + Python present
# --------------------------------------------------------------------------- #
command -v node   >/dev/null 2>&1 || fail "node not found — run: pkg install nodejs"
command -v python >/dev/null 2>&1 || fail "python not found — run: pkg install python"
command -v pm2    >/dev/null 2>&1 || fail "pm2 not found — run: npm install -g pm2"

log "Node  : $(node --version)"
log "Python: $(python --version 2>&1)"
log "PM2   : $(pm2 --version)"

# --------------------------------------------------------------------------- #
# JS Worker Agents — lint / syntax check
# --------------------------------------------------------------------------- #
log "Validating JS worker agents…"
AGENT_DIR="${REPO_DIR}/agent-x-core/agents"

for agent in \
  api-socket.js \
  content-generator.js \
  data-aggregator.js \
  infrastructure.js \
  orchestrator.js \
  publisher.js \
  watchdog.js; do
  agent_path="${AGENT_DIR}/${agent}"
  if [[ -f "${agent_path}" ]]; then
    node --check "${agent_path}" 2>/dev/null \
      && log "  ✔ ${agent}" \
      || warn "  ✘ ${agent} — syntax error detected"
  else
    warn "  – ${agent} not found (skipping)"
  fi
done

# --------------------------------------------------------------------------- #
# Python Agents — import check
# --------------------------------------------------------------------------- #
log "Validating Python agents…"

check_py() {
  local label="$1"
  local pyfile="$2"
  if [[ -f "${pyfile}" ]]; then
    python -c "
import ast, sys
try:
    ast.parse(open('${pyfile}').read())
    print('  \033[0;32m✔\033[0m ${label}')
except SyntaxError as e:
    print('  \033[0;31m✘\033[0m ${label} —', e)
    sys.exit(1)
" || true
  else
    echo -e "  ${YELLOW}–${RESET} ${label} (not found)"
  fi
}

check_py "intelligence_brain.py"  "${REPO_DIR}/core/intelligence_brain.py"
check_py "revenue_brain.py"       "${REPO_DIR}/core/revenue_brain.py"
check_py "revenue_engine.py"      "${REPO_DIR}/core/revenue_engine.py"
check_py "loop_engine.py"         "${REPO_DIR}/core/loop_engine.py"
check_py "supervisor.py"          "${REPO_DIR}/core/supervisor.py"
check_py "state_manager.py"       "${REPO_DIR}/core/state_manager.py"
check_py "task_registry.py"       "${REPO_DIR}/core/task_registry.py"
check_py "dashboard/app.py"       "${REPO_DIR}/dashboard/app.py"
check_py "builder_agent.py"       "${REPO_DIR}/agents/builder/builder_agent.py"
check_py "planner_agent.py"       "${REPO_DIR}/agents/planner/planner_agent.py"
check_py "researcher_agent.py"    "${REPO_DIR}/agents/researcher/researcher_agent.py"
check_py "revenue_agent.py"       "${REPO_DIR}/agents/revenue/revenue_agent.py"

# --------------------------------------------------------------------------- #
# Runtime directories
# --------------------------------------------------------------------------- #
log "Ensuring runtime directories exist…"
for dir in \
  "${REPO_DIR}/memory" \
  "${REPO_DIR}/data" \
  "${REPO_DIR}/generated" \
  "${REPO_DIR}/logs" \
  "${REPO_DIR}/products/deliverables" \
  "${REPO_DIR}/products/catalog"; do
  mkdir -p "${dir}"
  log "  ✔ ${dir}"
done

# --------------------------------------------------------------------------- #
# Permissions — make all scripts executable
# --------------------------------------------------------------------------- #
log "Setting script permissions…"
find "${REPO_DIR}/termux" -name "*.sh" -exec chmod +x {} \;
chmod +x "${REPO_DIR}/setup_agents.sh"   2>/dev/null || true
chmod +x "${REPO_DIR}/upgrade_agents.sh" 2>/dev/null || true
chmod +x "${REPO_DIR}/run.py"            2>/dev/null || true

# --------------------------------------------------------------------------- #
# Done
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${GREEN}✔ Agent setup complete!${RESET}"
echo ""
echo "  Start all services : bash termux/start.sh"
echo "  Check status       : bash termux/status.sh"
echo ""
