#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Agent Upgrade Script (Termux-compatible)
# Pulls latest code, reinstalls dependencies, and restarts running services.
#
# Previously contained hardcoded /usr paths and systemctl commands —
# replaced with $PREFIX-relative paths and PM2 restarts.
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

log()  { echo -e "${GREEN}[upgrade]${RESET} $*"; }
warn() { echo -e "${YELLOW}[warn]${RESET}    $*"; }
fail() { echo -e "${RED}[fail]${RESET}    $*"; exit 1; }

log "Agent X — Upgrade"
log "Repo: ${REPO_DIR}"

# --------------------------------------------------------------------------- #
# 1. Pull latest code (skip if --no-pull flag passed)
# --------------------------------------------------------------------------- #
if [[ "${1:-}" != "--no-pull" ]]; then
  if [[ -d "${REPO_DIR}/.git" ]]; then
    log "Pulling latest changes from git…"
    git -C "${REPO_DIR}" pull --rebase --autostash || warn "git pull failed — continuing with local files."
  else
    warn "Not a git repo — skipping git pull."
  fi
else
  log "--no-pull flag set — skipping git pull."
fi

# --------------------------------------------------------------------------- #
# 2. Stop running services gracefully
# --------------------------------------------------------------------------- #
log "Stopping running services…"
for svc in agent-x-core digital-twin dashboard webhook-listener; do
  pm2 stop "${svc}" 2>/dev/null && log "  stopped ${svc}" || true
done

# --------------------------------------------------------------------------- #
# 3. Upgrade pkg packages
# --------------------------------------------------------------------------- #
log "Upgrading pkg packages…"
pkg upgrade -y nodejs python 2>/dev/null || warn "pkg upgrade failed — continuing."

# --------------------------------------------------------------------------- #
# 4. Reinstall Node.js dependencies
# --------------------------------------------------------------------------- #
log "Reinstalling Node.js dependencies…"

npm_install() {
  local dir="$1"
  if [[ -f "${dir}/package.json" ]]; then
    log "  npm install → ${dir}"
    (cd "${dir}" && npm install --silent) || warn "  npm install failed in ${dir}"
  fi
}

npm_install "${REPO_DIR}"
npm_install "${REPO_DIR}/agent-x-core"
npm_install "${REPO_DIR}/digital-twin"
npm_install "${REPO_DIR}/communication"
npm_install "${REPO_DIR}/webhook-listener"

# Upgrade PM2 itself
log "Upgrading PM2…"
npm install -g pm2@latest 2>/dev/null || warn "PM2 upgrade failed — current version kept."
pm2 update 2>/dev/null || true

# --------------------------------------------------------------------------- #
# 5. Upgrade Python dependencies
# --------------------------------------------------------------------------- #
log "Upgrading Python dependencies…"
pip install --upgrade --quiet \
  flask \
  flask-socketio \
  flask-cors \
  eventlet \
  requests \
  pyyaml \
  python-dotenv \
  stripe \
  schedule \
  psutil \
  colorama \
  rich

if [[ -f "${REPO_DIR}/requirements.txt" ]]; then
  pip install --upgrade --quiet -r "${REPO_DIR}/requirements.txt" || \
    warn "Some requirements.txt packages failed — check manually."
fi

# --------------------------------------------------------------------------- #
# 6. Re-run agent validation
# --------------------------------------------------------------------------- #
log "Re-validating agents…"
bash "${REPO_DIR}/setup_agents.sh" || warn "setup_agents.sh reported issues — review above."

# --------------------------------------------------------------------------- #
# 7. Restart services
# --------------------------------------------------------------------------- #
log "Restarting services…"
bash "${REPO_DIR}/termux/start.sh" all

# --------------------------------------------------------------------------- #
# Done
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${GREEN}✔ Upgrade complete!${RESET}"
echo ""
bash "${REPO_DIR}/termux/status.sh"
