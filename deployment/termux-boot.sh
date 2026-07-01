#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux:Boot Entry Point
# ─────────────────────────────────
# Drop this file at:  ~/.termux/boot/agent-x-boot.sh
# Requires: Termux:Boot app (F-Droid — NOT Google Play)
#   https://f-droid.org/en/packages/com.termux.boot/
#
# NOTE: systemd is NOT available in Termux.  This file replaces:
#   deployment/agent-x-core.service
#   deployment/digital-twin.service
# =============================================================================

# Allow Android to finish booting before we do anything
sleep 10

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
HOME_DIR="${HOME:-/data/data/com.termux/files/home}"

# ── Locate repo ──────────────────────────────────────────────────────────────
# Adjust REPO_DIR if you cloned agent-x to a different location.
REPO_DIR="${HOME_DIR}/agent-x"

LOG_DIR="${REPO_DIR}/logs"
mkdir -p "${LOG_DIR}"
BOOT_LOG="${LOG_DIR}/boot.log"

# ── Redirect all output to log file ──────────────────────────────────────────
exec >> "${BOOT_LOG}" 2>&1
echo ""
echo "============================================="
echo " Agent X Termux boot — $(date)"
echo "============================================="

# ── Guard: repo must exist ────────────────────────────────────────────────────
if [[ ! -d "${REPO_DIR}" ]]; then
  echo "[boot] ERROR: Repo not found at ${REPO_DIR}"
  echo "[boot] Clone first: git clone <repo> ${REPO_DIR}"
  exit 1
fi

# ── Guard: node + pm2 must be present ────────────────────────────────────────
if ! command -v node >/dev/null 2>&1; then
  echo "[boot] ERROR: node not found. Run: pkg install nodejs"
  exit 1
fi
if ! command -v pm2 >/dev/null 2>&1; then
  echo "[boot] ERROR: pm2 not found. Run: npm install -g pm2"
  exit 1
fi

# ── Try to resurrect a previously saved PM2 process list ─────────────────────
echo "[boot] Attempting pm2 resurrect…"
if pm2 resurrect 2>/dev/null; then
  echo "[boot] PM2 process list restored."
else
  echo "[boot] No saved PM2 state — starting fresh…"
  bash "${REPO_DIR}/termux/start.sh" all
fi

echo "[boot] Done — $(date)"
