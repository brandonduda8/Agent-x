#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Termux Boot Script
# Place this file at:
#   ~/.termux/boot/agent-x-boot.sh
# Then install the Termux:Boot app and enable it so this runs on device boot.
#
# This replaces all systemd / @reboot cron / init.d approaches — none of those
# work in Termux without root.
#
# Installation:
#   mkdir -p ~/.termux/boot
#   cp termux/boot.sh ~/.termux/boot/agent-x-boot.sh
#   chmod +x ~/.termux/boot/agent-x-boot.sh
# =============================================================================

# Give Android/Termux a few seconds to fully initialise networking
sleep 8

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="${HOME}/agent-x"   # Adjust if your repo lives elsewhere

LOG_FILE="${REPO_DIR}/logs/boot.log"
mkdir -p "${REPO_DIR}/logs"

exec >> "${LOG_FILE}" 2>&1
echo "=== Agent X boot: $(date) ==="

# Restore PM2 process list that was saved by start.sh
pm2 resurrect || true

# If nothing was restored (first boot), start everything fresh
if ! pm2 list 2>/dev/null | grep -q "agent-x-core"; then
  echo "No saved PM2 state — running start.sh…"
  bash "${REPO_DIR}/termux/start.sh" all
fi

echo "=== Agent X boot complete: $(date) ==="
