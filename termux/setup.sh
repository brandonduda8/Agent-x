#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Bootstrap Setup Script
# Installs all required pkg + pip dependencies and prepares the environment.
# Run once after cloning: bash termux/setup.sh
# =============================================================================

set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME_DIR="${HOME:-/data/data/com.termux/files/home}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

log()  { echo -e "${GREEN}[setup]${RESET} $*"; }
warn() { echo -e "${YELLOW}[warn]${RESET}  $*"; }
fail() { echo -e "${RED}[fail]${RESET}  $*"; exit 1; }

# --------------------------------------------------------------------------- #
# 0. Sanity check — must run inside Termux
# --------------------------------------------------------------------------- #
if [[ ! -d "/data/data/com.termux" ]]; then
  fail "This script must be run inside Termux on Android."
fi

log "Agent X Termux setup starting…"
log "Repo root : ${REPO_DIR}"
log "PREFIX    : ${PREFIX}"
log "HOME      : ${HOME_DIR}"

# --------------------------------------------------------------------------- #
# 1. Update package index
# --------------------------------------------------------------------------- #
log "Updating pkg index…"
pkg update -y

# --------------------------------------------------------------------------- #
# 2. Core system packages
# --------------------------------------------------------------------------- #
log "Installing system packages…"
pkg install -y \
  bash \
  coreutils \
  curl \
  wget \
  git \
  nodejs \
  python \
  python-pip \
  make \
  clang \
  binutils \
  openssl \
  libffi \
  pkg-config \
  zip \
  unzip \
  procps \
  iproute2 \
  less \
  nano \
  jq

# --------------------------------------------------------------------------- #
# 3. Node.js — install / upgrade npm itself
# --------------------------------------------------------------------------- #
log "Upgrading npm…"
npm install -g npm@latest 2>/dev/null || warn "npm self-upgrade skipped (already current)"

# --------------------------------------------------------------------------- #
# 4. Global npm tools  (pm2, nodemon — no systemd needed)
# --------------------------------------------------------------------------- #
log "Installing global npm tools…"
npm install -g pm2 nodemon

# --------------------------------------------------------------------------- #
# 5. Python pip dependencies
# --------------------------------------------------------------------------- #
log "Installing Python dependencies from requirements.txt…"

# Ensure pip is up to date
python -m pip install --upgrade pip --quiet

# Termux-safe extras (no gcc-heavy packages by default)
pip install --quiet \
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

# Install repo requirements.txt if present
if [[ -f "${REPO_DIR}/requirements.txt" ]]; then
  log "Installing from requirements.txt…"
  pip install --quiet -r "${REPO_DIR}/requirements.txt" || \
    warn "Some requirements.txt packages failed — check manually."
fi

# --------------------------------------------------------------------------- #
# 6. Node.js project dependencies
# --------------------------------------------------------------------------- #
log "Installing Node.js project dependencies…"

install_npm() {
  local dir="$1"
  if [[ -f "${dir}/package.json" ]]; then
    log "  npm install → ${dir}"
    (cd "${dir}" && npm install --silent) || warn "npm install failed in ${dir}"
  fi
}

install_npm "${REPO_DIR}"
install_npm "${REPO_DIR}/agent-x-core"
install_npm "${REPO_DIR}/digital-twin"
install_npm "${REPO_DIR}/communication"
install_npm "${REPO_DIR}/webhook-listener"

# --------------------------------------------------------------------------- #
# 7. Create required runtime directories
# --------------------------------------------------------------------------- #
log "Creating runtime directories…"
mkdir -p \
  "${REPO_DIR}/memory" \
  "${REPO_DIR}/data" \
  "${REPO_DIR}/generated" \
  "${REPO_DIR}/logs" \
  "${REPO_DIR}/products/deliverables" \
  "${REPO_DIR}/products/catalog"

# --------------------------------------------------------------------------- #
# 8. Initialise blank state files (idempotent)
# --------------------------------------------------------------------------- #
init_json() {
  local file="$1"
  local default="${2:-{}}"
  if [[ ! -f "${file}" ]]; then
    echo "${default}" > "${file}"
    log "  created ${file}"
  fi
}

init_json "${REPO_DIR}/memory/state.json"  '{"status":"idle","agents":{}}'
init_json "${REPO_DIR}/memory/brain.json"  '{"tasks":[],"revenue":0}'
init_json "${REPO_DIR}/memory/tasks.json"  '[]'
init_json "${REPO_DIR}/data/db.json"       '{"products":[],"tasks":[]}'
init_json "${REPO_DIR}/data/revenue.json"  '{"total":0,"transactions":[]}'
init_json "${REPO_DIR}/data/projects.json" '[]'

# --------------------------------------------------------------------------- #
# 9. Write .env template if missing
# --------------------------------------------------------------------------- #
ENV_FILE="${REPO_DIR}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  log "Writing .env template…"
  cat > "${ENV_FILE}" <<'ENV'
# Agent X — Environment Variables
# Fill in real values before starting services.

# --- Core ports ---
PORT=3000
DIGITAL_TWIN_PORT=3002
DASHBOARD_PORT=5000

# --- Paths (auto-set for Termux) ---
AGENT_X_ROOT=__REPO_DIR__
MEMORY_DIR=__REPO_DIR__/memory
DATA_DIR=__REPO_DIR__/data
LOGS_DIR=__REPO_DIR__/logs
GENERATED_DIR=__REPO_DIR__/generated

# --- Stripe ---
STRIPE_SECRET_KEY=sk_test_REPLACE_ME
STRIPE_PUBLISHABLE_KEY=pk_test_REPLACE_ME
STRIPE_WEBHOOK_SECRET=whsec_REPLACE_ME

# --- LLM ---
OPENAI_API_KEY=REPLACE_ME
ANTHROPIC_API_KEY=REPLACE_ME

# --- Misc ---
NODE_ENV=development
LOG_LEVEL=info
ENV
  # Substitute real repo dir into .env
  sed -i "s|__REPO_DIR__|${REPO_DIR}|g" "${ENV_FILE}"
  log ".env written to ${ENV_FILE}"
else
  log ".env already exists — skipping."
fi

# --------------------------------------------------------------------------- #
# 10. Symlink convenience launcher
# --------------------------------------------------------------------------- #
LAUNCHER="${PREFIX}/bin/agent-x"
if [[ ! -f "${LAUNCHER}" ]]; then
  log "Creating agent-x launcher at ${LAUNCHER}…"
  cat > "${LAUNCHER}" <<LAUNCHER
#!/data/data/com.termux/files/usr/bin/bash
exec bash "${REPO_DIR}/termux/start.sh" "\$@"
LAUNCHER
  chmod +x "${LAUNCHER}"
fi

# --------------------------------------------------------------------------- #
# Done
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${GREEN}✔ Agent X setup complete!${RESET}"
echo ""
echo "  Next steps:"
echo "   1. Edit ${ENV_FILE} and fill in API keys"
echo "   2. Run:  agent-x start        (or: bash termux/start.sh)"
echo "   3. Run:  agent-x status       (or: bash termux/status.sh)"
echo ""
