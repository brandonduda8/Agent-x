#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Dev-Server Test Suite
# Validates that each service starts, binds its port, and responds to HTTP
# health checks within a configurable timeout.
#
# Usage:
#   bash termux/test-dev-server.sh              # test all services
#   bash termux/test-dev-server.sh core         # test agent-x-core only
#   bash termux/test-dev-server.sh twin         # test digital-twin only
#   bash termux/test-dev-server.sh dashboard    # test dashboard only
#   bash termux/test-dev-server.sh quick        # port-only checks (no start)
#   bash termux/test-dev-server.sh --no-start   # health-check only (assume running)
#
# Exit codes:
#   0  all checks passed
#   1  one or more checks failed
# =============================================================================

set -uo pipefail

# --------------------------------------------------------------------------- #
# Paths & config
# --------------------------------------------------------------------------- #
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"
LOG_DIR="${REPO_DIR}/logs"
REPORT_FILE="${LOG_DIR}/test-dev-server-$(date +%Y%m%d-%H%M%S).log"

# How long to wait (seconds) for a service to become reachable after start
STARTUP_TIMEOUT="${STARTUP_TIMEOUT:-30}"
# How long between polling attempts
POLL_INTERVAL=2
# Whether to launch services before testing (set to false with --no-start)
DO_START=true

# --------------------------------------------------------------------------- #
# Parse CLI args
# --------------------------------------------------------------------------- #
TARGET="${1:-all}"
for arg in "$@"; do
  case "${arg}" in
    --no-start) DO_START=false ;;
  esac
done

# --------------------------------------------------------------------------- #
# Colours & logging
# --------------------------------------------------------------------------- #
BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
DIM="\033[2m"
RESET="\033[0m"

mkdir -p "${LOG_DIR}"

_log() {
  local level="$1"; shift
  local msg="$*"
  local ts; ts="$(date '+%H:%M:%S')"
  echo -e "${msg}"
  # Strip ANSI for log file
  echo "[${ts}] $(echo -e "${msg}" | sed 's/\x1b\[[0-9;]*m//g')" >> "${REPORT_FILE}"
}

log()     { _log INFO   "${GREEN}  [PASS]${RESET}  $*"; }
info()    { _log INFO   "${CYAN}  [info]${RESET}  $*"; }
warn()    { _log WARN   "${YELLOW}  [WARN]${RESET}  $*"; }
fail()    { _log FAIL   "${RED}  [FAIL]${RESET}  $*"; }
section() { _log SECT   ""; _log SECT "${BOLD}${CYAN}── $* ──${RESET}"; }

# --------------------------------------------------------------------------- #
# Global pass/fail counters
# --------------------------------------------------------------------------- #
PASS=0
FAIL=0
SKIP=0

pass() { (( PASS++ )) || true; log "$*"; }
fail_test() { (( FAIL++ )) || true; fail "$*"; }
skip_test() { (( SKIP++ )) || true; warn "  [SKIP]  $*"; }

# --------------------------------------------------------------------------- #
# Load .env
# --------------------------------------------------------------------------- #
if [[ -f "${ENV_FILE}" ]]; then
  set -a; source "${ENV_FILE}"; set +a
else
  warn ".env not found — using default port values"
fi

CORE_PORT="${PORT:-3000}"
TWIN_PORT="${DIGITAL_TWIN_PORT:-3002}"
DASH_PORT="${DASHBOARD_PORT:-5000}"
WEBHOOK_PORT="${WEBHOOK_PORT:-3003}"

# --------------------------------------------------------------------------- #
# Helper: check if a TCP port is listening
# --------------------------------------------------------------------------- #
port_listening() {
  local port="$1"
  # Try ss first (iproute2), fall back to netstat (net-tools), then curl
  if command -v ss >/dev/null 2>&1; then
    ss -tlnH 2>/dev/null | grep -q ":${port}[[:space:]]" && return 0
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -tlnp 2>/dev/null | grep -q ":${port}[[:space:]]" && return 0
  fi
  # Last resort: attempt a TCP connection
  (echo >/dev/tcp/127.0.0.1/"${port}") >/dev/null 2>&1 && return 0
  return 1
}

# --------------------------------------------------------------------------- #
# Helper: HTTP health check with retry
# --------------------------------------------------------------------------- #
http_check() {
  local label="$1"
  local url="$2"
  local expected_code="${3:-200}"

  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time 5 \
    --retry 2 \
    --retry-delay 1 \
    "${url}" 2>/dev/null || echo "000")

  if [[ "${code}" == "${expected_code}" ]] || \
     [[ "${expected_code}" == "2xx" && "${code}" =~ ^2 ]]; then
    pass "${label} — HTTP ${code} ← ${url}"
    return 0
  else
    fail_test "${label} — HTTP ${code} (expected ${expected_code}) ← ${url}"
    return 1
  fi
}

# --------------------------------------------------------------------------- #
# Helper: wait for port to open, then health-check
# --------------------------------------------------------------------------- #
wait_for_service() {
  local name="$1"
  local port="$2"
  local health_url="$3"
  local timeout="${4:-${STARTUP_TIMEOUT}}"

  info "Waiting for ${name} on port ${port} (timeout ${timeout}s)…"

  local elapsed=0
  while (( elapsed < timeout )); do
    if port_listening "${port}"; then
      info "${name} port ${port} is open after ${elapsed}s"
      break
    fi
    sleep "${POLL_INTERVAL}"
    (( elapsed += POLL_INTERVAL )) || true
  done

  if ! port_listening "${port}"; then
    fail_test "${name} — port ${port} did not open within ${timeout}s"
    return 1
  fi

  # Give the HTTP server a moment to fully initialise its routes
  sleep 1
  http_check "${name} health endpoint" "${health_url}" "2xx"
}

# --------------------------------------------------------------------------- #
# Helper: verify PM2 process exists and is online
# --------------------------------------------------------------------------- #
pm2_status_check() {
  local svc="$1"
  if ! command -v pm2 >/dev/null 2>&1; then
    skip_test "PM2 not available — cannot check ${svc} status"
    return
  fi
  local status
  status=$(pm2 jlist 2>/dev/null | \
    python3 -c "
import sys, json
try:
  procs = json.load(sys.stdin)
  match = [p for p in procs if p.get('name') == '${svc}']
  print(match[0]['pm2_env']['status'] if match else 'missing')
except Exception as e:
  print('parse-error')
" 2>/dev/null || echo "unknown")

  case "${status}" in
    online)   pass  "PM2: ${svc} → ${status}" ;;
    missing)  fail_test "PM2: ${svc} → not registered" ;;
    stopped)  warn   "PM2: ${svc} → stopped (not an error if --no-start)" ;;
    *)        warn   "PM2: ${svc} → ${status}" ;;
  esac
}

# --------------------------------------------------------------------------- #
# Section 1: Pre-flight environment checks
# --------------------------------------------------------------------------- #
section "1. Pre-flight environment checks"

echo ""
{
  # Running in Termux?
  if [[ -d "/data/data/com.termux" ]]; then
    pass "Running inside Termux ✔"
  else
    warn "Not running in Termux — some checks may behave differently"
  fi

  # Node.js
  if command -v node >/dev/null 2>&1; then
    NODE_VER=$(node --version 2>/dev/null)
    pass "node available — ${NODE_VER}"
    # ARM architecture
    ARCH=$(uname -m 2>/dev/null || echo "unknown")
    info "Architecture: ${ARCH}"
    case "${ARCH}" in
      aarch64|armv7l|armv8l)
        info "ARM architecture detected — checking for known node compatibility issues"
        # node ≥ 18 is fully supported on aarch64 via Termux packages
        NODE_MAJOR=$(echo "${NODE_VER}" | tr -d 'v' | cut -d. -f1)
        if (( NODE_MAJOR >= 18 )); then
          pass "Node.js ${NODE_MAJOR}.x — ARM64 fully supported ✔"
        elif (( NODE_MAJOR >= 16 )); then
          warn "Node.js ${NODE_MAJOR}.x on ARM — upgrade recommended (pkg upgrade nodejs)"
        else
          fail_test "Node.js ${NODE_MAJOR}.x — too old for ARM, upgrade required"
        fi
        ;;
      x86_64)
        info "x86_64 (emulation or server) — no ARM-specific constraints"
        ;;
    esac
  else
    fail_test "node not found — run: pkg install nodejs"
  fi

  # npm
  if command -v npm >/dev/null 2>&1; then
    NPM_VER=$(npm --version 2>/dev/null)
    pass "npm available — v${NPM_VER}"
  else
    fail_test "npm not found"
  fi

  # python
  PYTHON=""
  for candidate in python3 python; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      PYTHON="${candidate}"
      break
    fi
  done
  if [[ -n "${PYTHON}" ]]; then
    PY_VER=$("${PYTHON}" --version 2>&1)
    pass "Python available — ${PY_VER} (${PYTHON})"
  else
    fail_test "Python not found — run: pkg install python"
  fi

  # pm2
  if command -v pm2 >/dev/null 2>&1; then
    PM2_VER=$(pm2 --version 2>/dev/null || echo "unknown")
    pass "pm2 available — v${PM2_VER}"
  else
    fail_test "pm2 not found — run: npm install -g pm2"
  fi

  # curl
  if command -v curl >/dev/null 2>&1; then
    pass "curl available"
  else
    fail_test "curl not found — run: pkg install curl"
  fi
}

# --------------------------------------------------------------------------- #
# Section 2: File / directory integrity
# --------------------------------------------------------------------------- #
section "2. Required files and directories"

check_file() {
  local path="$1"
  if [[ -f "${path}" ]]; then
    pass "File exists: ${path##"${REPO_DIR}/"}"
  else
    fail_test "Missing file: ${path##"${REPO_DIR}/"}"
  fi
}

check_dir() {
  local path="$1"
  if [[ -d "${path}" ]]; then
    pass "Dir exists: ${path##"${REPO_DIR}/"}"
  else
    fail_test "Missing dir: ${path##"${REPO_DIR}/"} (run: bash termux/setup.sh)"
  fi
}

check_dir  "${REPO_DIR}/agent-x-core"
check_dir  "${REPO_DIR}/digital-twin"
check_dir  "${REPO_DIR}/dashboard"
check_dir  "${REPO_DIR}/memory"
check_dir  "${REPO_DIR}/logs"
check_dir  "${REPO_DIR}/data"

check_file "${REPO_DIR}/.env"
check_file "${REPO_DIR}/agent-x-core/index.js"
check_file "${REPO_DIR}/agent-x-core/package.json"
check_file "${REPO_DIR}/digital-twin/index.js"
check_file "${REPO_DIR}/digital-twin/package.json"
check_file "${REPO_DIR}/dashboard/app.py"
check_file "${REPO_DIR}/dashboard/templates/index.html"

# node_modules
for svc in agent-x-core digital-twin; do
  if [[ -d "${REPO_DIR}/${svc}/node_modules" ]]; then
    pass "${svc}/node_modules exists"
  else
    fail_test "${svc}/node_modules missing — run: cd ${svc} && npm install"
  fi
done

# --------------------------------------------------------------------------- #
# Section 3: Port availability (pre-start)
# --------------------------------------------------------------------------- #
section "3. Port availability check (pre-start)"

check_port_free() {
  local name="$1"
  local port="$2"
  if port_listening "${port}"; then
    warn "${name}: port ${port} already in use — service may already be running"
    # Not a failure — could be our own PM2 process
  else
    pass "${name}: port ${port} is free"
  fi
}

check_port_free "agent-x-core"  "${CORE_PORT}"
check_port_free "digital-twin"  "${TWIN_PORT}"
check_port_free "dashboard"     "${DASH_PORT}"
check_port_free "webhook"       "${WEBHOOK_PORT}"

# Detect port conflicts between services
if [[ "${TWIN_PORT}" == "${DASH_PORT}" ]]; then
  warn "PORT CONFLICT: digital-twin (${TWIN_PORT}) and dashboard (${DASH_PORT}) share the same port!"
  warn "  Set DIGITAL_TWIN_PORT and DASHBOARD_PORT to different values in .env"
fi

# --------------------------------------------------------------------------- #
# Section 4: ARM / Termux-specific permission checks
# --------------------------------------------------------------------------- #
section "4. ARM / Termux permission checks"

# Check /proc/net/tcp is readable (needed by ss/netstat)
if [[ -r "/proc/net/tcp" ]]; then
  pass "/proc/net/tcp readable (port detection will work)"
else
  warn "/proc/net/tcp not readable — falling back to TCP connection probe for port checks"
fi

# Check /dev/null is writable (basic sanity)
if [[ -w "/dev/null" ]]; then
  pass "/dev/null writable"
else
  fail_test "/dev/null not writable — Android permissions issue"
fi

# Check exec permission on key scripts
for script in \
  "${REPO_DIR}/termux/start.sh" \
  "${REPO_DIR}/termux/stop.sh" \
  "${REPO_DIR}/termux/run_dashboard.sh"; do
  if [[ -x "${script}" ]]; then
    pass "Executable: ${script##"${REPO_DIR}/"}"
  else
    warn "Not executable: ${script##"${REPO_DIR}/"} — fixing…"
    chmod +x "${script}" 2>/dev/null && \
      pass "  Fixed exec bit on ${script##"${REPO_DIR}/"}" || \
      fail_test "  Could not chmod ${script##"${REPO_DIR}/"}"
  fi
done

# Check that we can write to $REPO_DIR (storage permissions)
WRITE_TEST="${REPO_DIR}/logs/.write-test-$$"
if touch "${WRITE_TEST}" 2>/dev/null; then
  rm -f "${WRITE_TEST}"
  pass "Write access to repo directory confirmed"
else
  fail_test "Cannot write to ${REPO_DIR} — check Android storage permissions"
  fail_test "  Try: termux-setup-storage"
fi

# Check wake lock hint (informational — not fatal)
if command -v termux-wake-lock >/dev/null 2>&1; then
  info "termux-wake-lock available — services will persist in background"
  info "  Recommendation: run 'termux-wake-lock' before starting services"
else
  warn "termux-wake-lock not found — processes may be killed by Android"
  warn "  Install Termux:API and run: termux-wake-lock"
fi

# --------------------------------------------------------------------------- #
# Section 5: Node.js module integrity checks (syntax parse)
# --------------------------------------------------------------------------- #
section "5. Node.js entry-point syntax check"

node_syntax_check() {
  local file="$1"
  local label="${file##"${REPO_DIR}/"}"
  if [[ ! -f "${file}" ]]; then
    skip_test "Syntax check skipped (missing): ${label}"
    return
  fi
  local err
  err=$(node --check "${file}" 2>&1) && \
    pass "Syntax OK: ${label}" || \
    fail_test "Syntax error in ${label}:
      ${err}"
}

node_syntax_check "${REPO_DIR}/agent-x-core/index.js"
node_syntax_check "${REPO_DIR}/digital-twin/index.js"
node_syntax_check "${REPO_DIR}/agent-x-core/agents/orchestrator.js"
node_syntax_check "${REPO_DIR}/agent-x-core/agents/content-generator.js"
node_syntax_check "${REPO_DIR}/agent-x-core/agents/data-aggregator.js"

# --------------------------------------------------------------------------- #
# Section 6: Python module import checks
# --------------------------------------------------------------------------- #
section "6. Python import checks"

py_import_check() {
  local module="$1"
  if [[ -z "${PYTHON}" ]]; then
    skip_test "Python not available — skipping import check for ${module}"
    return
  fi
  if "${PYTHON}" -c "import ${module}" >/dev/null 2>&1; then
    pass "Python import OK: ${module}"
  else
    fail_test "Python import FAILED: ${module} — run: pip install ${module}"
  fi
}

py_import_check "flask"
py_import_check "flask_socketio"
py_import_check "requests"
py_import_check "dotenv"

# Check dashboard app.py has no syntax errors
if [[ -n "${PYTHON}" && -f "${REPO_DIR}/dashboard/app.py" ]]; then
  PY_SYNTAX_ERR=$("${PYTHON}" -m py_compile "${REPO_DIR}/dashboard/app.py" 2>&1) && \
    pass "Python syntax OK: dashboard/app.py" || \
    fail_test "Python syntax error in dashboard/app.py:
      ${PY_SYNTAX_ERR}"
fi

# --------------------------------------------------------------------------- #
# Section 7: Start services (if DO_START=true)
# --------------------------------------------------------------------------- #
section "7. Service startup"

if [[ "${DO_START}" == "false" ]]; then
  warn "Skipping service start (--no-start flag or 'quick' mode)"
elif [[ "${TARGET}" == "quick" ]]; then
  warn "Quick mode — skipping service start"
  DO_START=false
else
  if ! command -v pm2 >/dev/null 2>&1; then
    fail_test "pm2 not found — cannot start services. Run: npm install -g pm2"
    DO_START=false
  else
    START_SCRIPT="${REPO_DIR}/termux/start.sh"
    if [[ ! -x "${START_SCRIPT}" ]]; then
      chmod +x "${START_SCRIPT}"
    fi

    case "${TARGET}" in
      core)
        info "Starting agent-x-core only…"
        bash "${START_SCRIPT}" core 2>&1 | tail -5 || \
          fail_test "start.sh core returned non-zero"
        ;;
      twin)
        info "Starting digital-twin only…"
        bash "${START_SCRIPT}" twin 2>&1 | tail -5 || \
          fail_test "start.sh twin returned non-zero"
        ;;
      dashboard)
        info "Starting dashboard only…"
        bash "${START_SCRIPT}" dashboard 2>&1 | tail -5 || \
          fail_test "start.sh dashboard returned non-zero"
        ;;
      all|*)
        info "Starting all services via termux/start.sh…"
        bash "${START_SCRIPT}" all 2>&1 | tail -10 || \
          fail_test "start.sh all returned non-zero"
        ;;
    esac
    pass "start.sh completed without fatal error"
  fi
fi

# --------------------------------------------------------------------------- #
# Section 8: Health checks
# --------------------------------------------------------------------------- #
section "8. Service health checks"

run_core_checks() {
  wait_for_service "agent-x-core" "${CORE_PORT}" \
    "http://localhost:${CORE_PORT}/health" "${STARTUP_TIMEOUT}"

  # Additional endpoint probes
  http_check "agent-x-core /api/tasks" \
    "http://localhost:${CORE_PORT}/api/tasks" "2xx"
}

run_twin_checks() {
  wait_for_service "digital-twin" "${TWIN_PORT}" \
    "http://localhost:${TWIN_PORT}/health" "${STARTUP_TIMEOUT}"
}

run_dashboard_checks() {
  wait_for_service "dashboard" "${DASH_PORT}" \
    "http://localhost:${DASH_PORT}/" "${STARTUP_TIMEOUT}"
}

case "${TARGET}" in
  core)        run_core_checks ;;
  twin)        run_twin_checks ;;
  dashboard)   run_dashboard_checks ;;
  quick)
    info "Quick mode — checking currently-bound ports only"
    port_listening "${CORE_PORT}" && \
      http_check "agent-x-core" "http://localhost:${CORE_PORT}/health" "2xx" || \
      warn "agent-x-core not reachable on port ${CORE_PORT}"
    port_listening "${TWIN_PORT}" && \
      http_check "digital-twin" "http://localhost:${TWIN_PORT}/health" "2xx" || \
      warn "digital-twin not reachable on port ${TWIN_PORT}"
    port_listening "${DASH_PORT}" && \
      http_check "dashboard" "http://localhost:${DASH_PORT}/" "2xx" || \
      warn "dashboard not reachable on port ${DASH_PORT}"
    ;;
  all|*)
    [[ "${DO_START}" == "false" ]] && {
      # Just health-check whatever is already running
      run_core_checks || true
      run_twin_checks || true
      run_dashboard_checks || true
    } || {
      run_core_checks
      run_twin_checks
      run_dashboard_checks
    }
    ;;
esac

# --------------------------------------------------------------------------- #
# Section 9: PM2 process status verification
# --------------------------------------------------------------------------- #
section "9. PM2 process status"

if [[ "${DO_START}" == "true" ]] || pm2 list 2>/dev/null | grep -q "online"; then
  case "${TARGET}" in
    core)      pm2_status_check "agent-x-core" ;;
    twin)      pm2_status_check "digital-twin" ;;
    dashboard) pm2_status_check "dashboard" ;;
    all|*)
      pm2_status_check "agent-x-core"
      pm2_status_check "digital-twin"
      pm2_status_check "dashboard"
      ;;
  esac
else
  skip_test "No PM2 processes running — skipping status checks"
fi

# --------------------------------------------------------------------------- #
# Section 10: Log file verification
# --------------------------------------------------------------------------- #
section "10. Log file checks"

check_log() {
  local svc="$1"
  local log_file="${LOG_DIR}/${svc}.log"
  if [[ -f "${log_file}" ]]; then
    SIZE=$(wc -c < "${log_file}" 2>/dev/null || echo "0")
    LINES=$(wc -l < "${log_file}" 2>/dev/null || echo "0")
    pass "Log exists: logs/${svc}.log (${SIZE} bytes, ${LINES} lines)"
    # Check for common fatal errors in logs
    if grep -qi "EADDRINUSE\|Cannot find module\|SyntaxError\|Error: " \
       "${log_file}" 2>/dev/null | head -3; then
      warn "  Possible errors found in ${svc}.log — review above"
    fi
    # Show last 3 lines
    info "  Last lines of ${svc}.log:"
    tail -n 3 "${log_file}" 2>/dev/null | sed 's/^/    /'
  else
    if [[ "${DO_START}" == "true" ]]; then
      fail_test "Log not created: logs/${svc}.log"
    else
      skip_test "Log absent (service not started): logs/${svc}.log"
    fi
  fi
}

case "${TARGET}" in
  core)      check_log "agent-x-core" ;;
  twin)      check_log "digital-twin" ;;
  dashboard) check_log "dashboard" ;;
  all|*)
    check_log "agent-x-core"
    check_log "digital-twin"
    check_log "dashboard"
    ;;
esac

# --------------------------------------------------------------------------- #
# Section 11: ARM-specific runtime anomaly detection
# --------------------------------------------------------------------------- #
section "11. ARM runtime anomaly detection"

ARCH=$(uname -m 2>/dev/null || echo "unknown")
if [[ "${ARCH}" == "aarch64" || "${ARCH}" == "armv7l" ]]; then

  # Native addon check — bcrypt, sodium etc. often fail on ARM if not pre-built
  info "Checking for native Node.js addons (ARM pre-build issues)…"
  for svc_dir in "${REPO_DIR}/agent-x-core" "${REPO_DIR}/digital-twin"; do
    if [[ -d "${svc_dir}/node_modules" ]]; then
      # Find any .node binary addons
      NATIVE_COUNT=$(find "${svc_dir}/node_modules" -name "*.node" 2>/dev/null | wc -l || echo "0")
      if (( NATIVE_COUNT > 0 )); then
        info "  Found ${NATIVE_COUNT} native addon(s) in ${svc_dir##"${REPO_DIR}/"}"
        find "${svc_dir}/node_modules" -name "*.node" 2>/dev/null | head -5 | \
          while read -r addon; do
            if file "${addon}" 2>/dev/null | grep -q "ARM aarch64\|ARM,"; then
              pass "  Native addon compiled for ARM: ${addon##"${svc_dir}/node_modules/"}"
            elif file "${addon}" 2>/dev/null | grep -q "x86-64\|x86_64"; then
              fail_test "  x86_64 binary in ARM environment: ${addon##"${svc_dir}/node_modules/"}"
              warn "    Fix: cd ${svc_dir} && npm rebuild"
            else
              info "  Addon (arch unknown): ${addon##"${svc_dir}/node_modules/"}"
            fi
          done
      else
        pass "  No native addons in ${svc_dir##"${REPO_DIR}/"} (safe)"
      fi
    fi
  done

  # Check available memory (agents may OOM on low-RAM Android devices)
  if [[ -r "/proc/meminfo" ]]; then
    MEM_FREE_KB=$(grep MemAvailable /proc/meminfo 2>/dev/null | awk '{print $2}' || echo "0")
    MEM_FREE_MB=$(( MEM_FREE_KB / 1024 ))
    if (( MEM_FREE_MB >= 512 )); then
      pass "Available RAM: ${MEM_FREE_MB} MB (sufficient for dev server)"
    elif (( MEM_FREE_MB >= 256 )); then
      warn "Available RAM: ${MEM_FREE_MB} MB — low, consider closing other apps"
      warn "  If services OOM-crash, add --max-old-space-size=256 to NODE_OPTIONS"
    else
      fail_test "Available RAM: ${MEM_FREE_MB} MB — critically low, services will likely crash"
      warn "  Export: NODE_OPTIONS=--max-old-space-size=128"
    fi
  fi

  # Check disk space in repo (npm install / logs can fill /data quickly)
  DISK_FREE_KB=$(df -k "${REPO_DIR}" 2>/dev/null | tail -1 | awk '{print $4}' || echo "0")
  DISK_FREE_MB=$(( DISK_FREE_KB / 1024 ))
  if (( DISK_FREE_MB >= 500 )); then
    pass "Free disk space: ${DISK_FREE_MB} MB"
  elif (( DISK_FREE_MB >= 100 )); then
    warn "Free disk space: ${DISK_FREE_MB} MB — limited"
  else
    fail_test "Free disk space: ${DISK_FREE_MB} MB — critically low"
  fi

  # Check CPU architecture compatibility for Python packages
  info "Checking Python wheel architecture…"
  if [[ -n "${PYTHON}" ]]; then
    PY_PLATFORM=$("${PYTHON}" -c "import platform; print(platform.machine())" 2>/dev/null || echo "unknown")
    pass "Python platform.machine() → ${PY_PLATFORM}"
    if [[ "${PY_PLATFORM}" == "aarch64" ]]; then
      pass "Python running native ARM64 — no emulation overhead"
    fi
  fi

else
  info "Not on ARM (${ARCH}) — skipping ARM-specific checks"
fi

# --------------------------------------------------------------------------- #
# Section 12: Graceful stop (cleanup — only if we started the services)
# --------------------------------------------------------------------------- #
section "12. Post-test cleanup"

if [[ "${DO_START}" == "true" && "${TARGET}" != "quick" ]]; then
  info "Tests complete. Services left running for continued use."
  info "  To stop: bash termux/stop.sh"
  info "  To view logs: bash termux/logs.sh"
else
  info "No services were started by this test — nothing to clean up."
fi

# --------------------------------------------------------------------------- #
# Final summary
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${CYAN}           Agent X Dev-Server Test Results             ${RESET}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${GREEN}${BOLD}PASSED:${RESET}  ${PASS}"
echo -e "  ${RED}${BOLD}FAILED:${RESET}  ${FAIL}"
echo -e "  ${YELLOW}${BOLD}SKIPPED:${RESET} ${SKIP}"
echo ""
echo -e "  Full log: ${DIM}${REPORT_FILE}${RESET}"
echo ""

if (( FAIL > 0 )); then
  echo -e "  ${RED}${BOLD}RESULT: FAIL${RESET} — ${FAIL} check(s) failed. See log for details."
  echo ""
  echo -e "  ${YELLOW}Troubleshooting reference:${RESET}"
  echo -e "    cat ${REPO_DIR}/TERMUX-TEST-REPORT.md"
  exit 1
else
  echo -e "  ${GREEN}${BOLD}RESULT: PASS${RESET} — all checks passed."
  echo ""
  exit 0
fi
