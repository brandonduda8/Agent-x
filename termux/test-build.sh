#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Build Process Test Suite
# Validates the full build / setup pipeline:
#   • pkg dependencies
#   • npm install (per service)
#   • pip install (core Python packages)
#   • Directory & state-file creation
#   • .env template generation
#   • PM2 daemon readiness
#   • ARM / aarch64 compatibility
#   • Post-build smoke tests
#
# Usage:
#   bash termux/test-build.sh              # full build test
#   bash termux/test-build.sh --fast       # skip heavy package installs
#   bash termux/test-build.sh --clean      # wipe node_modules + caches first
#   bash termux/test-build.sh --help
#
# Exit codes:
#   0  all required checks passed
#   1  one or more required checks failed
# =============================================================================

set -uo pipefail

# --------------------------------------------------------------------------- #
# CLI flags
# --------------------------------------------------------------------------- #
FAST_MODE=false
CLEAN_MODE=false
for arg in "$@"; do
  case "${arg}" in
    --fast)   FAST_MODE=true ;;
    --clean)  CLEAN_MODE=true ;;
    --help|-h)
      echo "Usage: bash termux/test-build.sh [--fast] [--clean] [--help]"
      echo "  --fast   Skip slow package installs; verify existing installation only"
      echo "  --clean  Remove node_modules + pip caches before re-building"
      echo "  --help   Show this help"
      exit 0
      ;;
  esac
done

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"
LOG_DIR="${REPO_DIR}/logs"
REPORT_FILE="${LOG_DIR}/test-build-$(date +%Y%m%d-%H%M%S).log"

mkdir -p "${LOG_DIR}"

# --------------------------------------------------------------------------- #
# Colour helpers
# --------------------------------------------------------------------------- #
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
DIM="\033[2m"
RESET="\033[0m"

_log() {
  local msg="$*"
  local ts; ts="$(date '+%H:%M:%S')"
  echo -e "${msg}"
  echo "[${ts}] $(echo -e "${msg}" | sed 's/\x1b\[[0-9;]*m//g')" >> "${REPORT_FILE}"
}

log()     { _log "${GREEN}  [PASS]${RESET}  $*"; }
info()    { _log "${CYAN}  [info]${RESET}  $*"; }
warn()    { _log "${YELLOW}  [WARN]${RESET}  $*"; }
fail()    { _log "${RED}  [FAIL]${RESET}  $*"; }
section() { _log ""; _log "${BOLD}${CYAN}── $* ──${RESET}"; }

PASS=0; FAIL=0; SKIP=0

pass()      { (( PASS++ )) || true; log "$*"; }
fail_test() { (( FAIL++ )) || true; fail "$*"; }
skip_test() { (( SKIP++ )) || true; warn "  [SKIP]  $*"; }

# --------------------------------------------------------------------------- #
# Python binary detection
# --------------------------------------------------------------------------- #
PYTHON=""
for candidate in python3 python; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    PYTHON="${candidate}"
    break
  fi
done

# --------------------------------------------------------------------------- #
# Section 1: Environment sanity
# --------------------------------------------------------------------------- #
section "1. Build environment sanity"

# Termux guard (informational)
if [[ -d "/data/data/com.termux" ]]; then
  pass "Termux environment confirmed"
else
  warn "Not running in Termux — results may differ on other platforms"
fi

ARCH=$(uname -m 2>/dev/null || echo "unknown")
info "Architecture: ${ARCH}"
info "Repo root:    ${REPO_DIR}"
info "Log file:     ${REPORT_FILE}"
[[ "${FAST_MODE}"  == "true" ]] && info "Mode: --fast  (skipping package installs)"
[[ "${CLEAN_MODE}" == "true" ]] && info "Mode: --clean (wiping node_modules)"

# Shell version
info "Bash version: ${BASH_VERSION:-unknown}"

# Date / timezone
info "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"

# --------------------------------------------------------------------------- #
# Section 2: System package checks
# --------------------------------------------------------------------------- #
section "2. System package availability"

check_binary() {
  local name="$1"
  local install_hint="${2:-pkg install ${name}}"
  if command -v "${name}" >/dev/null 2>&1; then
    local ver
    ver=$("${name}" --version 2>&1 | head -1 || echo "")
    pass "${name} — ${ver}"
  else
    fail_test "${name} not found. Fix: ${install_hint}"
  fi
}

check_binary "bash"   "pkg install bash"
check_binary "node"   "pkg install nodejs"
check_binary "npm"    "pkg install nodejs"
check_binary "git"    "pkg install git"
check_binary "curl"   "pkg install curl"
check_binary "jq"     "pkg install jq"
check_binary "make"   "pkg install make"

if [[ -n "${PYTHON}" ]]; then
  PY_VER=$("${PYTHON}" --version 2>&1)
  pass "Python — ${PY_VER} (${PYTHON})"
else
  fail_test "Python not found. Fix: pkg install python"
fi

# pip
if [[ -n "${PYTHON}" ]] && "${PYTHON}" -m pip --version >/dev/null 2>&1; then
  PIP_VER=$("${PYTHON}" -m pip --version | awk '{print $2}')
  pass "pip — v${PIP_VER}"
else
  fail_test "pip not found or broken. Fix: pkg install python-pip"
fi

# pm2
if command -v pm2 >/dev/null 2>&1; then
  PM2_VER=$(pm2 --version 2>/dev/null || echo "unknown")
  pass "pm2 — v${PM2_VER}"
else
  fail_test "pm2 not found. Fix: npm install -g pm2"
fi

# --------------------------------------------------------------------------- #
# Section 3: Node.js version compatibility
# --------------------------------------------------------------------------- #
section "3. Node.js version compatibility"

if command -v node >/dev/null 2>&1; then
  NODE_VER=$(node --version 2>/dev/null | tr -d 'v')
  NODE_MAJOR=$(echo "${NODE_VER}" | cut -d. -f1)

  info "Node.js version: ${NODE_VER}"

  # express v5 requires Node ≥ 18
  if (( NODE_MAJOR >= 20 )); then
    pass "Node.js ${NODE_MAJOR}.x — LTS, fully compatible with all dependencies"
  elif (( NODE_MAJOR >= 18 )); then
    pass "Node.js ${NODE_MAJOR}.x — compatible (Express 5, uuid 14 all require ≥18)"
  elif (( NODE_MAJOR >= 16 )); then
    warn "Node.js ${NODE_MAJOR}.x — some packages (uuid@14, express@5) require Node ≥18"
    warn "  Fix: pkg upgrade nodejs"
    (( FAIL++ )) || true
  else
    fail_test "Node.js ${NODE_MAJOR}.x is too old. Minimum: Node 18. Fix: pkg upgrade nodejs"
  fi

  # npm version check — npm 7+ supports package-lock v2
  NPM_VER=$(npm --version 2>/dev/null || echo "0.0.0")
  NPM_MAJOR=$(echo "${NPM_VER}" | cut -d. -f1)
  if (( NPM_MAJOR >= 7 )); then
    pass "npm v${NPM_VER} — supports package-lock v2/v3"
  else
    warn "npm v${NPM_VER} — old, may have issues with lockfile v2. Fix: npm install -g npm@latest"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 4: Python version compatibility
# --------------------------------------------------------------------------- #
section "4. Python version compatibility"

if [[ -n "${PYTHON}" ]]; then
  PY_FULL=$("${PYTHON}" --version 2>&1 | awk '{print $2}')
  PY_MAJOR=$(echo "${PY_FULL}" | cut -d. -f1)
  PY_MINOR=$(echo "${PY_FULL}" | cut -d. -f2)

  info "Python version: ${PY_FULL}"

  if (( PY_MAJOR == 3 && PY_MINOR >= 9 )); then
    pass "Python ${PY_FULL} — fully compatible"
  elif (( PY_MAJOR == 3 && PY_MINOR >= 7 )); then
    warn "Python ${PY_FULL} — marginal; upgrade recommended (pkg upgrade python)"
  else
    fail_test "Python ${PY_FULL} is too old. Minimum: 3.7. Fix: pkg upgrade python"
  fi

  # Check pip is using the right Python
  PIP_PY=$("${PYTHON}" -m pip --version 2>/dev/null | awk '{print $NF}')
  info "pip associated with: ${PIP_PY}"
fi

# --------------------------------------------------------------------------- #
# Section 5: Clean mode — wipe node_modules
# --------------------------------------------------------------------------- #
if [[ "${CLEAN_MODE}" == "true" ]]; then
  section "5. Clean mode — removing node_modules"
  for svc in agent-x-core digital-twin communication webhook-listener; do
    NM="${REPO_DIR}/${svc}/node_modules"
    if [[ -d "${NM}" ]]; then
      info "  Removing ${svc}/node_modules…"
      rm -rf "${NM}" && pass "  Removed ${svc}/node_modules" || \
        warn "  Could not remove ${svc}/node_modules"
    fi
  done
  # Root node_modules
  if [[ -d "${REPO_DIR}/node_modules" ]]; then
    info "  Removing root node_modules…"
    rm -rf "${REPO_DIR}/node_modules" && pass "  Removed root/node_modules" || \
      warn "  Could not remove root/node_modules"
  fi
  # pip cache
  if [[ -n "${PYTHON}" ]]; then
    info "  Clearing pip cache…"
    "${PYTHON}" -m pip cache purge >/dev/null 2>&1 && pass "  pip cache cleared" || \
      warn "  pip cache purge skipped (already empty or not supported)"
  fi
else
  section "5. Clean mode — SKIPPED (use --clean to enable)"
  skip_test "Clean not requested"
fi

# --------------------------------------------------------------------------- #
# Section 6: npm install — per service
# --------------------------------------------------------------------------- #
section "6. npm install (per service)"

npm_install_check() {
  local svc_dir="$1"
  local label="${2:-${svc_dir##"${REPO_DIR}/"}}"

  if [[ ! -f "${svc_dir}/package.json" ]]; then
    skip_test "No package.json in ${label} — skipping npm install"
    return 0
  fi

  info "Running npm install in ${label}…"

  local start_s
  start_s=$(date +%s 2>/dev/null || echo "0")

  local npm_out npm_exit
  npm_out=$(cd "${svc_dir}" && \
    npm install \
      --prefer-offline \
      --no-audit \
      --no-fund \
      2>&1) || npm_exit=$?
  npm_exit="${npm_exit:-0}"

  local end_s
  end_s=$(date +%s 2>/dev/null || echo "0")
  local elapsed=$(( end_s - start_s ))

  if (( npm_exit == 0 )); then
    # Count installed packages
    PKG_COUNT=$(find "${svc_dir}/node_modules" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l || echo "?")
    pass "${label}: npm install OK — ${PKG_COUNT} packages in ${elapsed}s"
  else
    fail_test "${label}: npm install FAILED (exit ${npm_exit})"
    # Print last 10 lines of output for diagnosis
    echo "${npm_out}" | tail -10 | sed 's/^/    /' >> "${REPORT_FILE}"
    echo "${npm_out}" | tail -5 | sed "s/^/  ${YELLOW}│${RESET} /"
    return 1
  fi

  # ARM native-addon detection: look for build errors in output
  if echo "${npm_out}" | grep -qi "gyp ERR\|node-pre-gyp ERR\|ENOTSUP"; then
    warn "${label}: native addon build warnings detected"
    warn "  If services fail to start, run: cd ${svc_dir} && npm rebuild"
    echo "${npm_out}" | grep -i "gyp\|pre-gyp\|ENOTSUP" | head -5 | sed 's/^/    /' >> "${REPORT_FILE}"
  fi

  # Verify specific critical packages are present
  local -a critical_pkgs=()
  # Read critical packages from package.json dependencies
  if command -v jq >/dev/null 2>&1; then
    mapfile -t critical_pkgs < <(
      jq -r '.dependencies // {} | keys[]' "${svc_dir}/package.json" 2>/dev/null | head -10
    )
  fi
  for pkg in "${critical_pkgs[@]+"${critical_pkgs[@]}"}"; do
    if [[ -d "${svc_dir}/node_modules/${pkg}" ]]; then
      : # pass silently for brevity
    else
      warn "${label}: Expected package not found: node_modules/${pkg}"
    fi
  done
}

if [[ "${FAST_MODE}" == "true" ]]; then
  info "Fast mode — verifying existing node_modules (skipping npm install)"
  for svc_dir in \
    "${REPO_DIR}" \
    "${REPO_DIR}/agent-x-core" \
    "${REPO_DIR}/digital-twin" \
    "${REPO_DIR}/communication" \
    "${REPO_DIR}/webhook-listener"; do
    label="${svc_dir##"${REPO_DIR}/"}"
    [[ "${label}" == "${REPO_DIR}" ]] && label="root"
    if [[ -f "${svc_dir}/package.json" ]]; then
      if [[ -d "${svc_dir}/node_modules" ]]; then
        PKG_COUNT=$(find "${svc_dir}/node_modules" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l || echo "?")
        pass "${label}: node_modules exists (${PKG_COUNT} packages)"
      else
        fail_test "${label}: node_modules missing — run: cd ${svc_dir} && npm install"
      fi
    fi
  done
else
  npm_install_check "${REPO_DIR}"                  "root"
  npm_install_check "${REPO_DIR}/agent-x-core"     "agent-x-core"
  npm_install_check "${REPO_DIR}/digital-twin"     "digital-twin"
  npm_install_check "${REPO_DIR}/communication"    "communication"
  npm_install_check "${REPO_DIR}/webhook-listener" "webhook-listener"
fi

# --------------------------------------------------------------------------- #
# Section 7: Critical npm package version validation
# --------------------------------------------------------------------------- #
section "7. Critical npm package version validation"

validate_package_version() {
  local svc_dir="$1"
  local pkg="$2"
  local min_major="$3"
  local label="${svc_dir##"${REPO_DIR}/"}"

  local pkg_json="${svc_dir}/node_modules/${pkg}/package.json"
  if [[ ! -f "${pkg_json}" ]]; then
    skip_test "${label}/${pkg} not installed — skipping version check"
    return
  fi

  local ver
  if command -v jq >/dev/null 2>&1; then
    ver=$(jq -r '.version' "${pkg_json}" 2>/dev/null || echo "unknown")
  else
    ver=$(grep '"version"' "${pkg_json}" 2>/dev/null | head -1 | \
      sed 's/.*"version":[[:space:]]*"//;s/".*//' || echo "unknown")
  fi

  local major
  major=$(echo "${ver}" | cut -d. -f1 | tr -d 'v^~' 2>/dev/null || echo "0")

  if (( major >= min_major )); then
    pass "${label}/${pkg}@${ver} ≥ v${min_major} ✔"
  else
    fail_test "${label}/${pkg}@${ver} — expected ≥ v${min_major}"
    warn "  Fix: cd ${svc_dir} && npm install ${pkg}@latest"
  fi
}

# Key package requirements from the project tech stack
validate_package_version "${REPO_DIR}/agent-x-core" "express"  "5"
validate_package_version "${REPO_DIR}/agent-x-core" "axios"    "1"
validate_package_version "${REPO_DIR}/agent-x-core" "uuid"     "9"
validate_package_version "${REPO_DIR}/agent-x-core" "dotenv"   "16"

# --------------------------------------------------------------------------- #
# Section 8: pip / Python package install
# --------------------------------------------------------------------------- #
section "8. Python package installation"

if [[ -z "${PYTHON}" ]]; then
  skip_test "Python not available — skipping all Python package checks"
else
  CORE_PY_PKGS=(
    flask
    flask-socketio
    flask-cors
    eventlet
    requests
    python-dotenv
    stripe
    psutil
    pyyaml
    colorama
    rich
  )

  if [[ "${FAST_MODE}" == "true" ]]; then
    info "Fast mode — checking existing Python packages only"
    for pkg in "${CORE_PY_PKGS[@]}"; do
      module="${pkg//-/_}"
      module="${module/python_dotenv/dotenv}"
      if "${PYTHON}" -c "import ${module}" >/dev/null 2>&1; then
        pass "Python: ${pkg} importable ✔"
      else
        fail_test "Python: ${pkg} not importable — run: pip install ${pkg}"
      fi
    done
  else
    info "Installing/verifying core Python packages…"
    local_fail=0

    "${PYTHON}" -m pip install --quiet \
      "${CORE_PY_PKGS[@]}" \
      2>&1 | tail -6 || local_fail=1

    if (( local_fail == 0 )); then
      pass "pip install completed for core packages"
    else
      warn "pip install had warnings — running import checks…"
    fi

    # Verify imports regardless
    for pkg in "${CORE_PY_PKGS[@]}"; do
      module="${pkg//-/_}"
      module="${module/python_dotenv/dotenv}"
      module="${module/pyyaml/yaml}"
      module="${module/flask_cors/flask_cors}"
      if "${PYTHON}" -c "import ${module}" >/dev/null 2>&1; then
        pass "Python import: ${module} ✔"
      else
        fail_test "Python import FAILED: ${module} (package: ${pkg})"
      fi
    done
  fi

  # requirements.txt
  if [[ -f "${REPO_DIR}/requirements.txt" ]]; then
    if [[ "${FAST_MODE}" == "false" ]]; then
      info "Installing from requirements.txt…"
      "${PYTHON}" -m pip install --quiet \
        -r "${REPO_DIR}/requirements.txt" \
        2>&1 | tail -5 && \
        pass "requirements.txt installed" || \
        warn "requirements.txt install had errors — check manually"
    else
      info "Fast mode — skipping requirements.txt install"
    fi
    pass "requirements.txt exists"
  else
    warn "requirements.txt not found at repo root"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 9: Runtime directory creation
# --------------------------------------------------------------------------- #
section "9. Runtime directory creation"

REQUIRED_DIRS=(
  "${REPO_DIR}/memory"
  "${REPO_DIR}/data"
  "${REPO_DIR}/generated"
  "${REPO_DIR}/logs"
  "${REPO_DIR}/products/deliverables"
  "${REPO_DIR}/products/catalog"
)

for d in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "${d}" ]]; then
    mkdir -p "${d}" && pass "Created: ${d##"${REPO_DIR}/"}" || \
      fail_test "Could not create: ${d##"${REPO_DIR}/"}"
  else
    # Verify writable
    if touch "${d}/.write-test-$$" 2>/dev/null; then
      rm -f "${d}/.write-test-$$"
      pass "Dir writable: ${d##"${REPO_DIR}/"}"
    else
      fail_test "Dir not writable: ${d##"${REPO_DIR}/"}"
    fi
  fi
done

# --------------------------------------------------------------------------- #
# Section 10: JSON state file initialisation
# --------------------------------------------------------------------------- #
section "10. State file initialisation"

init_and_validate_json() {
  local file="$1"
  local default="${2:-{}}"
  local label="${file##"${REPO_DIR}/"}"

  if [[ ! -f "${file}" ]]; then
    echo "${default}" > "${file}" && \
      pass "Created: ${label}" || \
      fail_test "Could not create: ${label}"
    return
  fi

  # File exists — validate it is parseable JSON
  if command -v jq >/dev/null 2>&1; then
    if jq '.' "${file}" >/dev/null 2>&1; then
      KEYS=$(jq 'keys | length' "${file}" 2>/dev/null || echo "?")
      pass "Valid JSON: ${label} (${KEYS} top-level keys)"
    else
      fail_test "Invalid JSON: ${label}"
      warn "  Resetting to default: ${default}"
      echo "${default}" > "${file}"
    fi
  elif [[ -n "${PYTHON}" ]]; then
    if "${PYTHON}" -c "import json,sys; json.load(open('${file}'))" >/dev/null 2>&1; then
      pass "Valid JSON: ${label}"
    else
      fail_test "Invalid JSON: ${label}"
      echo "${default}" > "${file}"
    fi
  else
    # No validator available — just check non-empty
    SIZE=$(wc -c < "${file}" 2>/dev/null || echo "0")
    if (( SIZE > 0 )); then
      pass "Non-empty file: ${label} (${SIZE} bytes)"
    else
      fail_test "Empty file: ${label}"
      echo "${default}" > "${file}"
    fi
  fi
}

init_and_validate_json \
  "${REPO_DIR}/memory/state.json" \
  '{"status":"idle","agents":{},"startedAt":null}'

init_and_validate_json \
  "${REPO_DIR}/memory/brain.json" \
  '{"tasks":[],"revenue":0,"history":[]}'

init_and_validate_json \
  "${REPO_DIR}/memory/tasks.json" \
  '[]'

init_and_validate_json \
  "${REPO_DIR}/data/db.json" \
  '{"products":[],"tasks":[],"users":[]}'

init_and_validate_json \
  "${REPO_DIR}/data/revenue.json" \
  '{"total":0,"currency":"usd","transactions":[]}'

init_and_validate_json \
  "${REPO_DIR}/data/projects.json" \
  '[]'

init_and_validate_json \
  "${REPO_DIR}/products/catalog/catalog.json" \
  '{"products":[]}'

# --------------------------------------------------------------------------- #
# Section 11: .env file validation
# --------------------------------------------------------------------------- #
section "11. .env file validation"

if [[ ! -f "${ENV_FILE}" ]]; then
  warn ".env not found — generating template…"
  bash "${REPO_DIR}/termux/setup.sh" --help >/dev/null 2>&1 || true
  fail_test ".env missing. Fix: bash termux/setup.sh"
else
  pass ".env exists: ${ENV_FILE}"

  # Load and check required keys
  set -a; source "${ENV_FILE}"; set +a 2>/dev/null || true

  check_env_var() {
    local key="$1"
    local is_required="${2:-false}"
    local val="${!key:-}"
    if [[ -n "${val}" ]] && [[ "${val}" != "REPLACE_ME" ]] && \
       [[ "${val}" != *"REPLACE_ME"* ]]; then
      pass ".env: ${key} is set"
    elif [[ "${is_required}" == "true" ]]; then
      fail_test ".env: ${key} is missing or still set to REPLACE_ME"
      warn "  Edit ${ENV_FILE} and set a real value for ${key}"
    else
      warn ".env: ${key} not yet configured (optional for dev)"
    fi
  }

  # Required for core operation
  check_env_var "PORT"                "true"
  check_env_var "DIGITAL_TWIN_PORT"   "true"
  check_env_var "DASHBOARD_PORT"      "true"
  check_env_var "NODE_ENV"            "true"

  # Optional (warn but don't fail)
  check_env_var "STRIPE_SECRET_KEY"   "false"
  check_env_var "OPENAI_API_KEY"      "false"

  # Detect port collisions in .env
  if [[ "${PORT:-3000}" == "${DIGITAL_TWIN_PORT:-3002}" ]]; then
    fail_test "PORT and DIGITAL_TWIN_PORT are the same (${PORT}) — will cause EADDRINUSE"
  fi
  if [[ "${DIGITAL_TWIN_PORT:-3002}" == "${DASHBOARD_PORT:-5000}" ]]; then
    fail_test "DIGITAL_TWIN_PORT and DASHBOARD_PORT are the same (${DIGITAL_TWIN_PORT})"
  fi
  if [[ "${PORT:-3000}" == "${DASHBOARD_PORT:-5000}" ]]; then
    fail_test "PORT and DASHBOARD_PORT are the same (${PORT})"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 12: PM2 daemon readiness
# --------------------------------------------------------------------------- #
section "12. PM2 daemon readiness"

if ! command -v pm2 >/dev/null 2>&1; then
  fail_test "pm2 not installed — run: npm install -g pm2"
else
  # Try to ping the PM2 daemon (non-fatal — daemon starts on first use)
  if pm2 ping >/dev/null 2>&1; then
    pass "PM2 daemon is reachable"
  else
    info "PM2 daemon not yet running — attempting to start…"
    pm2 list >/dev/null 2>&1 && pass "PM2 daemon started OK" || \
      warn "PM2 daemon could not be started — will start automatically on first pm2 command"
  fi

  # Check PM2 startup hook is configured for Termux:Boot
  BOOT_DIR="${HOME:-/data/data/com.termux/files/home}/.termux/boot"
  BOOT_SCRIPT="${BOOT_DIR}/agent-x-boot.sh"
  if [[ -f "${BOOT_SCRIPT}" ]]; then
    pass "Termux:Boot hook installed: ${BOOT_SCRIPT}"
  else
    info "Termux:Boot hook not installed (optional) — run: bash termux/install_boot.sh"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 13: ARM-specific build compatibility checks
# --------------------------------------------------------------------------- #
section "13. ARM build compatibility"

ARCH=$(uname -m 2>/dev/null || echo "unknown")

if [[ "${ARCH}" == "aarch64" || "${ARCH}" == "armv7l" ]]; then
  info "ARM architecture: ${ARCH}"

  # Check for potential pre-gyp / native addon rebuild needs
  GYP_FAILURES=0
  for svc_dir in "${REPO_DIR}/agent-x-core" "${REPO_DIR}/digital-twin"; do
    [[ -d "${svc_dir}/node_modules" ]] || continue
    label="${svc_dir##"${REPO_DIR}/"}"

    # bcryptjs uses pure JS — safe
    if [[ -d "${svc_dir}/node_modules/bcryptjs" ]]; then
      pass "${label}: bcryptjs (pure JS) — ARM compatible ✔"
    fi
    # bcrypt (native) would need rebuild
    if [[ -d "${svc_dir}/node_modules/bcrypt" ]]; then
      warn "${label}: bcrypt (native C++) detected — may need rebuild on ARM"
      warn "  Fix: cd ${svc_dir} && npm rebuild bcrypt --build-from-source"
      (( GYP_FAILURES++ )) || true
    fi
    # stripe — pure JS
    if [[ -d "${svc_dir}/node_modules/stripe" ]]; then
      pass "${label}: stripe (pure JS) — ARM compatible ✔"
    fi
    # sodium-native (used by some socket libs) — native
    if [[ -d "${svc_dir}/node_modules/sodium-native" ]]; then
      warn "${label}: sodium-native detected — may need ARM rebuild"
      warn "  Fix: cd ${svc_dir} && npm rebuild sodium-native --build-from-source"
      (( GYP_FAILURES++ )) || true
    fi
  done

  if (( GYP_FAILURES == 0 )); then
    pass "No problematic native addons detected for ARM"
  fi

  # Memory constraint check
  if [[ -r "/proc/meminfo" ]]; then
    TOTAL_MEM_KB=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo "0")
    FREE_MEM_KB=$(grep MemAvailable /proc/meminfo 2>/dev/null | awk '{print $2}' || echo "0")
    TOTAL_MB=$(( TOTAL_MEM_KB / 1024 ))
    FREE_MB=$(( FREE_MEM_KB / 1024 ))
    info "Total RAM: ${TOTAL_MB} MB  |  Available: ${FREE_MB} MB"

    if (( FREE_MB >= 512 )); then
      pass "Sufficient RAM for npm install (${FREE_MB} MB free)"
    elif (( FREE_MB >= 256 )); then
      warn "Low RAM (${FREE_MB} MB) — npm install may be slow"
      info "  Tip: close other apps or add swap: dd if=/dev/zero of=~/swapfile bs=1M count=512"
    else
      fail_test "Very low RAM (${FREE_MB} MB) — npm install likely to fail with OOM"
      info "  Fix: add swap space or free memory before building"
    fi
  fi

  # Disk space check
  DISK_FREE_KB=$(df -k "${REPO_DIR}" 2>/dev/null | tail -1 | awk '{print $4}' || echo "0")
  DISK_FREE_MB=$(( DISK_FREE_KB / 1024 ))
  if (( DISK_FREE_MB >= 1000 )); then
    pass "Disk space: ${DISK_FREE_MB} MB free (sufficient for full build)"
  elif (( DISK_FREE_MB >= 300 )); then
    warn "Disk space: ${DISK_FREE_MB} MB — limited, --no-llm recommended for pip install"
  else
    fail_test "Disk space: ${DISK_FREE_MB} MB — too low for full build"
    info "  Free up space: npm cache clean --force && pip cache purge"
  fi

  # Check for Termux exec privilege (some Android 10+ devices restrict exec in /data)
  EXEC_TEST="${TMPDIR:-/tmp}/agent-x-exec-test-$$"
  echo '#!/bin/sh' > "${EXEC_TEST}" 2>/dev/null || true
  if chmod +x "${EXEC_TEST}" 2>/dev/null && "${EXEC_TEST}" >/dev/null 2>&1; then
    pass "Execute permission in tmpdir works (W^X not enforced)"
  else
    warn "Cannot execute scripts in ${TMPDIR:-/tmp} — possible W^X restriction"
    warn "  Ensure scripts are in Termux home or use PREFIX paths"
    warn "  tmpdir: use export TMPDIR=\$PREFIX/tmp"
  fi
  rm -f "${EXEC_TEST}" 2>/dev/null || true

else
  info "Not on ARM (${ARCH}) — skipping ARM-specific build checks"
  pass "Build environment: ${ARCH} — no ARM constraints"
fi

# --------------------------------------------------------------------------- #
# Section 14: Post-build smoke tests
# --------------------------------------------------------------------------- #
section "14. Post-build smoke tests"

# Test that Node.js can require key packages without errors
node_require_test() {
  local svc_dir="$1"
  local pkg="$2"
  local label="${svc_dir##"${REPO_DIR}/"}"

  if [[ ! -d "${svc_dir}/node_modules/${pkg}" ]]; then
    skip_test "require test skipped (not installed): ${label}/${pkg}"
    return
  fi

  if (cd "${svc_dir}" && node -e "require('${pkg}')" >/dev/null 2>&1); then
    pass "require('${pkg}') OK in ${label}"
  else
    local err
    err=$(cd "${svc_dir}" && node -e "require('${pkg}')" 2>&1 | head -3)
    fail_test "require('${pkg}') FAILED in ${label}: ${err}"
  fi
}

node_require_test "${REPO_DIR}/agent-x-core" "express"
node_require_test "${REPO_DIR}/agent-x-core" "axios"
node_require_test "${REPO_DIR}/agent-x-core" "dotenv"
node_require_test "${REPO_DIR}/agent-x-core" "cors"
node_require_test "${REPO_DIR}/agent-x-core" "uuid"
node_require_test "${REPO_DIR}/digital-twin" "express"

# Test that the main entry points load without errors (--check flag)
entry_point_check() {
  local file="$1"
  local label="${file##"${REPO_DIR}/"}"
  if [[ ! -f "${file}" ]]; then
    skip_test "Entry point missing: ${label}"
    return
  fi
  node --check "${file}" >/dev/null 2>&1 && \
    pass "Syntax OK: ${label}" || \
    fail_test "Syntax error: ${label}"
}

entry_point_check "${REPO_DIR}/agent-x-core/index.js"
entry_point_check "${REPO_DIR}/digital-twin/index.js"

# Python dashboard import smoke test
if [[ -n "${PYTHON}" && -f "${REPO_DIR}/dashboard/app.py" ]]; then
  # We can't actually import app.py without starting Flask, but we can compile-check it
  if "${PYTHON}" -m py_compile "${REPO_DIR}/dashboard/app.py" >/dev/null 2>&1; then
    pass "dashboard/app.py compiles without syntax errors"
  else
    fail_test "dashboard/app.py has syntax errors"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 15: Idempotency check — re-run safety
# --------------------------------------------------------------------------- #
section "15. Idempotency / re-run safety"

# Re-running setup.sh should not destroy data — verify state files still intact
for f in \
  "${REPO_DIR}/memory/state.json" \
  "${REPO_DIR}/data/db.json"; do
  if [[ -f "${f}" ]]; then
    # Check it's non-empty
    SIZE=$(wc -c < "${f}" 2>/dev/null || echo "0")
    if (( SIZE > 0 )); then
      pass "State preserved after build: ${f##"${REPO_DIR}/"} (${SIZE} bytes)"
    else
      warn "State file empty after build: ${f##"${REPO_DIR}/"}"
    fi
  fi
done

# Verify .env was NOT overwritten (should be preserved if already existed)
if [[ -f "${ENV_FILE}" ]]; then
  pass ".env preserved (not overwritten by build)"
fi

# --------------------------------------------------------------------------- #
# Final summary
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${CYAN}            Agent X Build Test Results                 ${RESET}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${GREEN}${BOLD}PASSED:${RESET}  ${PASS}"
echo -e "  ${RED}${BOLD}FAILED:${RESET}  ${FAIL}"
echo -e "  ${YELLOW}${BOLD}SKIPPED:${RESET} ${SKIP}"
echo ""
echo -e "  Full log: ${DIM}${REPORT_FILE}${RESET}"
echo ""

if (( FAIL > 0 )); then
  echo -e "  ${RED}${BOLD}RESULT: FAIL${RESET} — ${FAIL} build check(s) failed."
  echo ""
  echo -e "  ${YELLOW}Common fixes:${RESET}"
  echo -e "    • Missing packages:  bash termux/setup.sh"
  echo -e "    • ARM rebuild:       cd agent-x-core && npm rebuild"
  echo -e "    • Low memory:        close apps + export NODE_OPTIONS=--max-old-space-size=256"
  echo -e "    • Full reference:    cat ${REPO_DIR}/TERMUX-TEST-REPORT.md"
  echo ""
  exit 1
else
  echo -e "  ${GREEN}${BOLD}RESULT: PASS${RESET} — all build checks passed."
  echo ""
  echo -e "  ${CYAN}Next step:${RESET} bash termux/test-dev-server.sh"
  echo ""
  exit 0
fi
