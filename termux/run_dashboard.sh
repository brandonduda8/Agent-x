#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Agent X — Dashboard Runner (called by PM2)
# Activates the Python environment and launches Flask + SocketIO dashboard.
# =============================================================================

set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_DIR}/.env"

# Load environment variables
if [[ -f "${ENV_FILE}" ]]; then
  set -a; source "${ENV_FILE}"; set +a
fi

export FLASK_APP="${REPO_DIR}/dashboard/app.py"
export FLASK_ENV="${NODE_ENV:-development}"
export DASHBOARD_PORT="${DASHBOARD_PORT:-5000}"

cd "${REPO_DIR}/dashboard"

# Prefer eventlet for async SocketIO; fall back to threading
exec python -c "
import os, sys
sys.path.insert(0, '${REPO_DIR}')
os.chdir('${REPO_DIR}/dashboard')
from app import app, socketio
port = int(os.environ.get('DASHBOARD_PORT', 5000))
socketio.run(app, host='0.0.0.0', port=port, debug=False)
"
