#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Install Termux:Boot hook
# Requires the Termux:Boot app to be installed from F-Droid.
# =============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOT_DIR="${HOME}/.termux/boot"
BOOT_TARGET="${BOOT_DIR}/agent-x-boot.sh"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RESET="\033[0m"

mkdir -p "${BOOT_DIR}"

cp "${REPO_DIR}/termux/boot.sh" "${BOOT_TARGET}"
# Patch REPO_DIR to the actual path of this installation
sed -i "s|REPO_DIR=\"\${HOME}/agent-x\"|REPO_DIR=\"${REPO_DIR}\"|" "${BOOT_TARGET}"
chmod +x "${BOOT_TARGET}"

echo -e "${GREEN}[boot]${RESET} Boot script installed at: ${BOOT_TARGET}"
echo ""
echo -e "${YELLOW}IMPORTANT:${RESET}"
echo "  1. Install Termux:Boot from F-Droid (NOT Google Play):"
echo "     https://f-droid.org/en/packages/com.termux.boot/"
echo "  2. Open Termux:Boot once to register the boot directory."
echo "  3. Agent X will auto-start on device reboot."
echo ""
echo "  Current boot script: ${BOOT_TARGET}"
