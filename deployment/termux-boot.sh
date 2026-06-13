#!/data/data/com.termux/files/usr/bin/bash
# Termux boot script for Agent X services

BASE="$HOME/agent-x"
COREPID="$BASE/.pids/agent-x-core.pid"
TWINPID="$BASE/.pids/digital-twin.pid"

mkdir -p "$BASE/.pids" "$BASE/logs"

start() {
  echo "Starting Agent X core..."
  nohup node "$BASE/agent-x-core/index.js" > "$BASE/logs/agent-x-core.log" 2>&1 &
  echo $! > "$COREPID"
  echo "Starting Digital Twin..."
  nohup node "$BASE/digital-twin/index.js" > "$BASE/logs/digital-twin.log" 2>&1 &
  echo $! > "$TWINPID"
  echo "Agent X started."
}

stop() {
  [ -f "$COREPID" ] && kill "$(cat "$COREPID")" 2>/dev/null || true
  [ -f "$TWINPID" ] && kill "$(cat "$TWINPID")" 2>/dev/null || true
  rm -f "$COREPID" "$TWINPID"
  echo "Agent X stopped."
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
esac
