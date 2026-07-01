#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Bootstrap Setup Script
# Installs all required pkg + pip dependencies and prepares the environment.
#
# Usage (run once after cloning):
#   bash termux/setup.sh            # full setup
#   bash termux/setup.sh --no-llm  # skip heavy LLM/transformers packages
#   bash termux/setup.sh --help
#
# Idempotent — safe to re-run at any time.
# =============================================================================

set -euo pipefail

# --------------------------------------------------------------------------- #
# CLI flags
# --------------------------------------------------------------------------- #
SKIP_LLM=false
for arg in "$@"; do
  case "${arg}" in
    --no-llm)  SKIP_LLM=true ;;
    --help|-h)
      echo "Usage: bash termux/setup.sh [--no-llm] [--help]"
      echo "  --no-llm   Skip transformers / torch (saves ~3 GB, speeds up install)"
      echo "  --help     Show this message"
      exit 0
      ;;
  esac
done

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME_DIR="${HOME:-/data/data/com.termux/files/home}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --------------------------------------------------------------------------- #
# Colours
# --------------------------------------------------------------------------- #
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

log()     { echo -e "${GREEN}[setup]${RESET} $*"; }
info()    { echo -e "${CYAN}[info]${RESET}  $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
fail()    { echo -e "${RED}[fail]${RESET}  $*"; exit 1; }
section() { echo ""; echo -e "${BOLD}${CYAN}── $* ──${RESET}"; }

# --------------------------------------------------------------------------- #
# 0. Sanity checks
# --------------------------------------------------------------------------- #
section "0. Sanity checks"

if [[ ! -d "/data/data/com.termux" ]]; then
  fail "This script must be run inside Termux on Android. Aborting."
fi

# Require bash >= 4 (Termux ships bash 5.x, but let's be explicit)
BASH_MAJOR="${BASH_VERSINFO[0]:-0}"
if (( BASH_MAJOR < 4 )); then
  fail "bash >= 4 required. Found: ${BASH_VERSION}. Run: pkg install bash"
fi

log "Termux detected ✔"
log "Repo root : ${REPO_DIR}"
log "PREFIX    : ${PREFIX}"
log "HOME      : ${HOME_DIR}"
[[ "${SKIP_LLM}" == "true" ]] && warn "LLM/transformers install SKIPPED (--no-llm)"

# --------------------------------------------------------------------------- #
# 1. Update package index
# --------------------------------------------------------------------------- #
section "1. Package index update"
log "Running pkg update…"
pkg update -y 2>&1 | tail -5

# --------------------------------------------------------------------------- #
# 2. Core system packages
# --------------------------------------------------------------------------- #
section "2. System packages"
log "Installing core system packages…"

SYSTEM_PKGS=(
  bash
  coreutils
  curl
  wget
  git
  nodejs
  python
  python-pip
  make
  clang
  binutils
  openssl
  libffi
  pkg-config
  zip
  unzip
  procps
  iproute2
  less
  nano
  jq
)

pkg install -y "${SYSTEM_PKGS[@]}" 2>&1 | grep -E "(Installing|already installed|Unpacking)" || true

# --------------------------------------------------------------------------- #
# 3. Verify Node.js and npm
# --------------------------------------------------------------------------- #
section "3. Node.js / npm verification"

command -v node >/dev/null 2>&1 || fail "node not found after pkg install. Check network and retry."
command -v npm  >/dev/null 2>&1 || fail "npm not found after pkg install."

NODE_VER=$(node --version 2>/dev/null || echo "unknown")
NPM_VER=$(npm --version 2>/dev/null || echo "unknown")
log "node ${NODE_VER}  |  npm ${NPM_VER}"

# Upgrade npm to latest (best-effort; non-fatal)
log "Upgrading npm…"
npm install -g npm@latest 2>/dev/null | tail -2 || warn "npm self-upgrade skipped (already current)."

# --------------------------------------------------------------------------- #
# 4. Global npm tools
# --------------------------------------------------------------------------- #
section "4. Global npm tools (pm2 / nodemon)"
log "Installing pm2 and nodemon globally…"
npm install -g pm2 nodemon 2>&1 | tail -5

PM2_VER=$(pm2 --version 2>/dev/null || echo "unknown")
log "pm2 version: ${PM2_VER}"

# --------------------------------------------------------------------------- #
# 5. Python verification
# --------------------------------------------------------------------------- #
section "5. Python / pip verification"

# Detect python binary (python3 preferred, fall back to python)
PYTHON=""
for candidate in python3 python; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    PYTHON="${candidate}"
    break
  fi
done
[[ -z "${PYTHON}" ]] && fail "Python not found. Run: pkg install python"

PY_VER=$("${PYTHON}" --version 2>&1 || echo "unknown")
log "Python: ${PY_VER}  (binary: ${PYTHON})"

# Upgrade pip
log "Upgrading pip…"
"${PYTHON}" -m pip install --upgrade pip --quiet

PIP_VER=$("${PYTHON}" -m pip --version 2>/dev/null | awk '{print $2}' || echo "unknown")
log "pip: ${PIP_VER}"

# --------------------------------------------------------------------------- #
# 6. Core Python dependencies
# --------------------------------------------------------------------------- #
section "6. Core Python dependencies"
log "Installing core Python packages…"

CORE_PY_PKGS=(
  flask
  flask-socketio
  flask-cors
  eventlet
  requests
  pyyaml
  python-dotenv
  stripe
  schedule
  psutil
  colorama
  rich
)

"${PYTHON}" -m pip install --quiet "${CORE_PY_PKGS[@]}" && \
  log "Core Python packages installed ✔" || \
  warn "Some core Python packages may have failed — check output above."

# --------------------------------------------------------------------------- #
# 7. LLM / AI packages (optional — skip with --no-llm)
# --------------------------------------------------------------------------- #
section "7. LLM / AI packages"

if [[ "${SKIP_LLM}" == "true" ]]; then
  warn "Skipping LLM/AI packages (--no-llm flag set)."
  warn "To install later:  pip install transformers sentencepiece accelerate"
else
  log "Installing LLM/AI packages (this may take several minutes)…"
  log "  Tip: use --no-llm to skip if disk/RAM is limited."

  # transformers without full torch (saves space on mobile)
  "${PYTHON}" -m pip install --quiet \
    transformers \
    sentencepiece \
    tokenizers \
    accelerate \
    2>&1 | tail -6 || warn "Some AI packages failed — torch/CUDA not available in Termux. Core functionality unaffected."

  # openai client (lightweight, useful even without local models)
  "${PYTHON}" -m pip install --quiet openai anthropic 2>/dev/null || \
    warn "openai/anthropic client install failed — install manually if needed."
fi

# --------------------------------------------------------------------------- #
# 8. requirements.txt (repo-level)
# --------------------------------------------------------------------------- #
section "8. requirements.txt"
if [[ -f "${REPO_DIR}/requirements.txt" ]]; then
  log "Installing from ${REPO_DIR}/requirements.txt…"
  "${PYTHON}" -m pip install --quiet -r "${REPO_DIR}/requirements.txt" 2>&1 | tail -6 || \
    warn "Some requirements.txt packages failed — check manually."
else
  warn "requirements.txt not found at repo root — skipping."
fi

# --------------------------------------------------------------------------- #
# 9. Node.js project dependencies (per-service npm install)
# --------------------------------------------------------------------------- #
section "9. Node.js project dependencies"

install_npm() {
  local dir="$1"
  local label="${2:-${dir}}"
  if [[ -f "${dir}/package.json" ]]; then
    log "  npm install → ${label}"
    (cd "${dir}" && npm install --silent --prefer-offline 2>&1 | tail -3) || \
      warn "  npm install failed in ${dir} — check package.json"
  else
    info "  No package.json in ${dir} — skipping."
  fi
}

install_npm "${REPO_DIR}"                       "root"
install_npm "${REPO_DIR}/agent-x-core"          "agent-x-core"
install_npm "${REPO_DIR}/digital-twin"          "digital-twin"
install_npm "${REPO_DIR}/communication"         "communication"
install_npm "${REPO_DIR}/webhook-listener"      "webhook-listener"

# --------------------------------------------------------------------------- #
# 10. Runtime directory creation
# --------------------------------------------------------------------------- #
section "10. Runtime directories"
log "Creating required runtime directories…"

DIRS=(
  "${REPO_DIR}/memory"
  "${REPO_DIR}/data"
  "${REPO_DIR}/generated"
  "${REPO_DIR}/logs"
  "${REPO_DIR}/products/deliverables"
  "${REPO_DIR}/products/catalog"
  "${REPO_DIR}/termux"
)

for d in "${DIRS[@]}"; do
  mkdir -p "${d}"
  log "  OK  ${d}"
done

# --------------------------------------------------------------------------- #
# 11. Initialise blank JSON state files (idempotent)
# --------------------------------------------------------------------------- #
section "11. State file initialisation"

init_json() {
  local file="$1"
  local default="${2:-{}}"
  if [[ ! -f "${file}" ]]; then
    echo "${default}" > "${file}"
    log "  created → ${file}"
  else
    info "  exists  → ${file}"
  fi
}

init_json "${REPO_DIR}/memory/state.json"  '{"status":"idle","agents":{},"startedAt":null}'
init_json "${REPO_DIR}/memory/brain.json"  '{"tasks":[],"revenue":0,"history":[]}'
init_json "${REPO_DIR}/memory/tasks.json"  '[]'
init_json "${REPO_DIR}/data/db.json"       '{"products":[],"tasks":[],"users":[]}'
init_json "${REPO_DIR}/data/revenue.json"  '{"total":0,"currency":"usd","transactions":[]}'
init_json "${REPO_DIR}/data/projects.json" '[]'
init_json "${REPO_DIR}/data/tasks.json"    '[]'

# --------------------------------------------------------------------------- #
# 12. Write .env template (only if missing)
# --------------------------------------------------------------------------- #
section "12. Environment variables (.env)"

ENV_FILE="${REPO_DIR}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  log "Writing .env template to ${ENV_FILE}…"
  cat > "${ENV_FILE}" <<ENV
# =============================================================================
# Agent X — Environment Variables
# Generated by termux/setup.sh on $(date)
# Fill in real values before starting services.
# =============================================================================

# --- Core service ports ---
PORT=3000
DIGITAL_TWIN_PORT=3002
DASHBOARD_PORT=5000
WEBHOOK_PORT=3003

# --- Paths (auto-resolved for this Termux install) ---
AGENT_X_ROOT=${REPO_DIR}
MEMORY_DIR=${REPO_DIR}/memory
DATA_DIR=${REPO_DIR}/data
LOGS_DIR=${REPO_DIR}/logs
GENERATED_DIR=${REPO_DIR}/generated

# --- Node environment ---
NODE_ENV=development
LOG_LEVEL=info

# --- Stripe (replace with real keys) ---
STRIPE_SECRET_KEY=sk_test_REPLACE_ME
STRIPE_PUBLISHABLE_KEY=pk_test_REPLACE_ME
STRIPE_WEBHOOK_SECRET=whsec_REPLACE_ME

# --- LLM providers (add whichever you use) ---
OPENAI_API_KEY=REPLACE_ME
ANTHROPIC_API_KEY=REPLACE_ME

# --- Misc ---
AGENT_LOOP_INTERVAL_MS=60000
MAX_CONCURRENT_AGENTS=4
ENV
  log ".env template written ✔"
  warn "Edit ${ENV_FILE} and fill in your API keys before starting."
else
  info ".env already exists — preserving existing file."
  info "  Location: ${ENV_FILE}"
fi

# --------------------------------------------------------------------------- #
# 13. Convenience launcher: agent-x command
# --------------------------------------------------------------------------- #
section "13. CLI launcher"

LAUNCHER="${PREFIX}/bin/agent-x"
if [[ ! -f "${LAUNCHER}" ]]; then
  log "Installing agent-x CLI to ${LAUNCHER}…"
  cat > "${LAUNCHER}" <<LAUNCHER
#!/data/data/com.termux/files/usr/bin/bash
# Agent X convenience launcher
exec bash "${REPO_DIR}/termux/start.sh" "\$@"
LAUNCHER
  chmod +x "${LAUNCHER}"
  log "  agent-x launcher installed ✔"
else
  info "  agent-x launcher already exists — skipping."
fi

# --------------------------------------------------------------------------- #
# 14. Termux:Boot hook hint
# --------------------------------------------------------------------------- #
section "14. Termux:Boot (optional auto-start)"
BOOT_DIR="${HOME_DIR}/.termux/boot"
if [[ -d "${BOOT_DIR}" ]]; then
  log "Termux:Boot directory found — running install_boot.sh…"
  bash "${REPO_DIR}/termux/install_boot.sh" || warn "install_boot.sh encountered an error — run manually."
else
  info "Termux:Boot not set up (directory not found)."
  info "  To enable auto-start on device reboot:"
  info "    1. Install Termux:Boot from F-Droid"
  info "    2. Open it once to register the boot directory"
  info "    3. Run:  bash termux/install_boot.sh"
fi

# --------------------------------------------------------------------------- #
# 15. Self-test — verify key binaries
# --------------------------------------------------------------------------- #
section "15. Self-test"

PASS=0
FAIL=0
check() {
  local label="$1"
  local cmd="$2"
  if eval "${cmd}" >/dev/null 2>&1; then
    echo -e "  ${GREEN}✔${RESET}  ${label}"
    (( PASS++ )) || true
  else
    echo -e "  ${RED}✘${RESET}  ${label}  ← FAILED"
    (( FAIL++ )) || true
  fi
}

check "bash"                "command -v bash"
check "node"                "command -v node"
check "npm"                 "command -v npm"
check "pm2"                 "command -v pm2"
check "python"              "command -v ${PYTHON}"
check "pip"                 "${PYTHON} -m pip --version"
check "git"                 "command -v git"
check "curl"                "command -v curl"
check "jq"                  "command -v jq"
check "flask (Python)"      "${PYTHON} -c 'import flask'"
check "flask_socketio"      "${PYTHON} -c 'import flask_socketio'"
check "requests (Python)"   "${PYTHON} -c 'import requests'"
check "psutil (Python)"     "${PYTHON} -c 'import psutil'"
check "yaml (Python)"       "${PYTHON} -c 'import yaml'"
check ".env exists"         "test -f '${REPO_DIR}/.env'"
check "memory/state.json"   "test -f '${REPO_DIR}/memory/state.json'"
check "data/db.json"        "test -f '${REPO_DIR}/data/db.json'"
check "logs dir"            "test -d '${REPO_DIR}/logs'"

if [[ "${SKIP_LLM}" == "false" ]]; then
  check "transformers (Python)" "${PYTHON} -c 'import transformers' 2>/dev/null"
fi

echo ""
echo -e "  Self-test: ${GREEN}${PASS} passed${RESET}  /  ${RED}${FAIL} failed${RESET}"

# --------------------------------------------------------------------------- #
# Done
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${GREEN}║   ✔  Agent X Termux setup complete!          ║${RESET}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${BOLD}Next steps:${RESET}"
echo ""
echo -e "   1. ${YELLOW}Edit your API keys:${RESET}"
echo -e "        nano ${ENV_FILE}"
echo ""
echo -e "   2. ${YELLOW}Start all services:${RESET}"
echo -e "        agent-x start"
echo -e "        # or: bash termux/start.sh"
echo ""
echo -e "   3. ${YELLOW}Check status:${RESET}"
echo -e "        bash termux/status.sh"
echo ""
echo -e "   4. ${YELLOW}View logs:${RESET}"
echo -e "        bash termux/logs.sh"
echo ""
echo -e "   5. ${YELLOW}Enable auto-start on reboot (optional):${RESET}"
echo -e "        bash termux/install_boot.sh"
echo ""

if (( FAIL > 0 )); then
  warn "${FAIL} self-test check(s) failed. Review the output above before starting services."
  exit 1
fi
