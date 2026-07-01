#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Master Test Runner
# Orchestrates the full test suite: build → dev-server → summary report.
#
# Usage:
#   bash termux/test-runner.sh                 # full suite (all tests)
#   bash termux/test-runner.sh --build-only    # build tests only
#   bash termux/test-runner.sh --server-only   # dev-server tests only
#   bash termux/test-runner.sh --fast          # skip installs / service start
#   bash termux/test-runner.sh --no-start      # skip service startup in server tests
#   bash termux/test-runner.sh --no-llm        # pass --no-llm flag to build setup
#   bash termux/test-runner.sh --help
#
# Exit codes:
#   0   all suites passed
#   1   one or more suites failed
#   2   runner setup error (scripts not found, etc.)
# =============================================================================

set -uo pipefail

# --------------------------------------------------------------------------- #
# Resolve repo root and script directory
# --------------------------------------------------------------------------- #
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_DIR="${REPO_DIR}/logs"
RUNNER_LOG="${LOG_DIR}/test-runner-$(date +%Y%m%d-%H%M%S).log"

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
  echo "[${ts}] $(echo -e "${msg}" | sed 's/\x1b\[[0-9;]*m//g')" >> "${RUNNER_LOG}"
}

info()    { _log "${CYAN}[runner]${RESET} $*"; }
warn()    { _log "${YELLOW}[runner]${RESET} $*"; }
section() { _log ""; _log "${BOLD}${CYAN}══════════════════════════════════════════════════${RESET}"; _log "${BOLD}${CYAN}  $*${RESET}"; _log "${BOLD}${CYAN}══════════════════════════════════════════════════${RESET}"; }

# --------------------------------------------------------------------------- #
# Parse CLI flags
# --------------------------------------------------------------------------- #
RUN_BUILD=true
RUN_SERVER=true
FAST_FLAG=""
NO_START_FLAG=""
NO_LLM_FLAG=""

for arg in "$@"; do
  case "${arg}" in
    --build-only)  RUN_SERVER=false ;;
    --server-only) RUN_BUILD=false ;;
    --fast)        FAST_FLAG="--fast" ;;
    --no-start)    NO_START_FLAG="--no-start" ;;
    --no-llm)      NO_LLM_FLAG="--no-llm" ;;
    --help|-h)
      echo ""
      echo "  Agent X — Master Test Runner"
      echo ""
      echo "  Usage:"
      echo "    bash termux/test-runner.sh [flags]"
      echo ""
      echo "  Flags:"
      echo "    --build-only    Run build tests only (skip dev-server tests)"
      echo "    --server-only   Run dev-server tests only (skip build tests)"
      echo "    --fast          Skip slow installs; verify existing state only"
      echo "    --no-start      Do not start services during server test"
      echo "    --no-llm        Skip LLM/transformers install during build"
      echo "    --help          Show this help message"
      echo ""
      echo "  Examples:"
      echo "    bash termux/test-runner.sh                  # full suite"
      echo "    bash termux/test-runner.sh --fast --no-start"
      echo "    bash termux/test-runner.sh --build-only --fast"
      echo ""
      exit 0
      ;;
    *)
      warn "Unknown flag: ${arg} (ignored)"
      ;;
  esac
done

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${CYAN}║          Agent X — Termux Full Test Suite               ║${RESET}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════╝${RESET}"
echo ""
info "Repo:      ${REPO_DIR}"
info "Runner log: ${RUNNER_LOG}"
info "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
info "Arch:      $(uname -m 2>/dev/null || echo 'unknown')"

NODE_VER=$(node --version 2>/dev/null || echo "not found")
PYTHON=$(command -v python3 || command -v python || echo "not found")
PY_VER=$("${PYTHON}" --version 2>&1 2>/dev/null || echo "not found")

info "Node.js:   ${NODE_VER}"
info "Python:    ${PY_VER}"
echo ""

SUITE_RESULTS=()   # array of "name:exit_code"
SUITE_LOGS=()      # array of "name:logfile"

# --------------------------------------------------------------------------- #
# Helper: run a test suite script and capture result
# --------------------------------------------------------------------------- #
run_suite() {
  local suite_name="$1"
  local script_path="$2"
  shift 2
  local extra_flags=("$@")

  if [[ ! -f "${script_path}" ]]; then
    warn "Test script not found: ${script_path}"
    SUITE_RESULTS+=("${suite_name}:2")
    return 2
  fi

  chmod +x "${script_path}" 2>/dev/null || true

  section "Suite: ${suite_name}"
  info "Script:  ${script_path##"${REPO_DIR}/"}"
  [[ "${#extra_flags[@]}" -gt 0 ]] && info "Flags:   ${extra_flags[*]}"
  echo ""

  local suite_start
  suite_start=$(date +%s 2>/dev/null || echo "0")

  local exit_code=0

  # Run the suite; tee output to both terminal and runner log
  bash "${script_path}" "${extra_flags[@]+"${extra_flags[@]}"}" \
    2>&1 | tee -a "${RUNNER_LOG}" || exit_code="${PIPESTATUS[0]}"

  # PIPESTATUS might not be set correctly when exit_code is set via ||
  # Re-capture exit status properly:
  if [[ "${exit_code}" == "0" ]]; then
    # Verify by checking the last log entry for RESULT: FAIL
    if grep -q "RESULT: FAIL" "${RUNNER_LOG}" 2>/dev/null; then
      # Only count failures from this suite's lines (rough heuristic)
      :
    fi
  fi

  local suite_end
  suite_end=$(date +%s 2>/dev/null || echo "0")
  local elapsed=$(( suite_end - suite_start ))

  if (( exit_code == 0 )); then
    _log ""
    _log "${GREEN}${BOLD}  ✔ Suite PASSED: ${suite_name}${RESET} (${elapsed}s)"
    SUITE_RESULTS+=("${suite_name}:0")
  else
    _log ""
    _log "${RED}${BOLD}  ✘ Suite FAILED: ${suite_name}${RESET} (exit ${exit_code}, ${elapsed}s)"
    SUITE_RESULTS+=("${suite_name}:${exit_code}")
  fi

  echo "" >> "${RUNNER_LOG}"
  return "${exit_code}"
}

# --------------------------------------------------------------------------- #
# Build test flags
# --------------------------------------------------------------------------- #
BUILD_FLAGS=()
[[ -n "${FAST_FLAG}" ]]  && BUILD_FLAGS+=("${FAST_FLAG}")
[[ -n "${NO_LLM_FLAG}" ]] && BUILD_FLAGS+=("${NO_LLM_FLAG}")

# --------------------------------------------------------------------------- #
# Server test flags
# --------------------------------------------------------------------------- #
SERVER_FLAGS=()
[[ -n "${FAST_FLAG}" ]]     && SERVER_FLAGS+=("quick")  # "quick" mode for test-dev-server
[[ -n "${NO_START_FLAG}" ]] && SERVER_FLAGS+=("--no-start")

# --------------------------------------------------------------------------- #
# Run suites
# --------------------------------------------------------------------------- #
OVERALL_EXIT=0

if [[ "${RUN_BUILD}" == "true" ]]; then
  run_suite \
    "Build Process" \
    "${SCRIPT_DIR}/test-build.sh" \
    "${BUILD_FLAGS[@]+"${BUILD_FLAGS[@]}"}" || OVERALL_EXIT=1
fi

if [[ "${RUN_SERVER}" == "true" ]]; then
  run_suite \
    "Dev Server" \
    "${SCRIPT_DIR}/test-dev-server.sh" \
    "${SERVER_FLAGS[@]+"${SERVER_FLAGS[@]}"}" || OVERALL_EXIT=1
fi

# --------------------------------------------------------------------------- #
# Final summary report
# --------------------------------------------------------------------------- #
section "Test Suite Summary"

TOTAL_SUITES="${#SUITE_RESULTS[@]}"
PASSED_SUITES=0
FAILED_SUITES=0

for result in "${SUITE_RESULTS[@]+"${SUITE_RESULTS[@]}"}"; do
  name="${result%%:*}"
  code="${result##*:}"
  if [[ "${code}" == "0" ]]; then
    (( PASSED_SUITES++ )) || true
    echo -e "  ${GREEN}✔${RESET}  ${name}"
  else
    (( FAILED_SUITES++ )) || true
    echo -e "  ${RED}✘${RESET}  ${name}  (exit ${code})"
  fi
done

echo ""
echo -e "  Suites run:    ${TOTAL_SUITES}"
echo -e "  ${GREEN}Suites passed: ${PASSED_SUITES}${RESET}"
echo -e "  ${RED}Suites failed: ${FAILED_SUITES}${RESET}"
echo ""
echo -e "  ${DIM}Runner log: ${RUNNER_LOG}${RESET}"
echo ""

# List all test logs generated
echo -e "${BOLD}Individual test logs:${RESET}"
for logf in "${LOG_DIR}"/test-build-*.log "${LOG_DIR}"/test-dev-server-*.log; do
  [[ -f "${logf}" ]] && echo -e "  ${DIM}${logf}${RESET}" || true
done
echo ""

if (( OVERALL_EXIT == 0 )); then
  echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════╗${RESET}"
  echo -e "${BOLD}${GREEN}║   ✔  All Agent X test suites PASSED!            ║${RESET}"
  echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════╝${RESET}"
  echo ""
  if [[ "${RUN_SERVER}" == "true" ]] && [[ -z "${NO_START_FLAG}" ]] && \
     [[ -z "${FAST_FLAG}" ]]; then
    echo -e "  ${CYAN}Services are running. Management commands:${RESET}"
    echo -e "    bash termux/status.sh     # live status"
    echo -e "    bash termux/logs.sh       # stream logs"
    echo -e "    bash termux/stop.sh       # stop all"
    echo ""
  fi
else
  echo -e "${BOLD}${RED}╔══════════════════════════════════════════════════╗${RESET}"
  echo -e "${BOLD}${RED}║   ✘  One or more test suites FAILED.            ║${RESET}"
  echo -e "${BOLD}${RED}╚══════════════════════════════════════════════════╝${RESET}"
  echo ""
  echo -e "  ${YELLOW}Next steps:${RESET}"
  echo -e "    1. Review the logs above for FAIL lines"
  echo -e "    2. Consult:  cat ${REPO_DIR}/TERMUX-TEST-REPORT.md"
  echo -e "    3. Re-run setup if needed: bash termux/setup.sh"
  echo -e "    4. Re-run this test: bash termux/test-runner.sh"
  echo ""
fi

exit "${OVERALL_EXIT}"
