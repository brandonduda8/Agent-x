#!/usr/bin/env python3
"""
Agent X — Python Process Manager (Termux-compatible)
=====================================================
Manages and monitors Agent X services without systemd or Docker.
Uses subprocess + psutil to spawn and supervise processes, writing
PID files under $REPO_DIR/logs/.

Replaces any previous systemctl / service invocations.

Usage:
    python process-manager.py start   [service]
    python process-manager.py stop    [service]
    python process-manager.py restart [service]
    python process-manager.py status
    python process-manager.py logs    [service] [--lines N]
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths — use $PREFIX for Termux, fall back to /usr on Linux
# --------------------------------------------------------------------------- #
PREFIX      = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
REPO_DIR    = Path(__file__).resolve().parent
ENV_FILE    = REPO_DIR / ".env"
LOGS_DIR    = REPO_DIR / "logs"
PID_DIR     = LOGS_DIR / "pids"
NODE_BIN    = Path(PREFIX) / "bin" / "node"
PYTHON_BIN  = sys.executable

# Fall back to system node if Termux node not found
if not NODE_BIN.exists():
    import shutil
    _node = shutil.which("node")
    NODE_BIN = Path(_node) if _node else Path("node")

LOGS_DIR.mkdir(parents=True, exist_ok=True)
PID_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------- #
# Service definitions (no systemd, no Docker)
# --------------------------------------------------------------------------- #
SERVICES = {
    "agent-x-core": {
        "cmd": [str(NODE_BIN), str(REPO_DIR / "agent-x-core" / "index.js")],
        "cwd": str(REPO_DIR / "agent-x-core"),
        "log": str(LOGS_DIR / "agent-x-core.log"),
    },
    "digital-twin": {
        "cmd": [str(NODE_BIN), str(REPO_DIR / "digital-twin" / "index.js")],
        "cwd": str(REPO_DIR / "digital-twin"),
        "log": str(LOGS_DIR / "digital-twin.log"),
    },
    "dashboard": {
        "cmd": [
            PYTHON_BIN, "-c",
            (
                "import os, sys; "
                f"sys.path.insert(0, '{REPO_DIR}'); "
                f"os.chdir('{REPO_DIR / 'dashboard'}'); "
                "from app import app, socketio; "
                "port = int(os.environ.get('DASHBOARD_PORT', 5000)); "
                "socketio.run(app, host='0.0.0.0', port=port, debug=False)"
            ),
        ],
        "cwd": str(REPO_DIR / "dashboard"),
        "log": str(LOGS_DIR / "dashboard.log"),
    },
    "webhook-listener": {
        "cmd": [str(NODE_BIN), str(REPO_DIR / "webhook-listener" / "index.js")],
        "cwd": str(REPO_DIR / "webhook-listener"),
        "log": str(LOGS_DIR / "webhook-listener.log"),
    },
}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _load_env() -> dict:
    """Parse .env file into a dict and merge with os.environ."""
    env = os.environ.copy()
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _pid_file(name: str) -> Path:
    return PID_DIR / f"{name}.pid"


def _read_pid(name: str) -> int | None:
    pf = _pid_file(name)
    if pf.exists():
        try:
            return int(pf.read_text().strip())
        except ValueError:
            pass
    return None


def _write_pid(name: str, pid: int):
    _pid_file(name).write_text(str(pid))


def _clear_pid(name: str):
    pf = _pid_file(name)
    if pf.exists():
        pf.unlink()


def _is_running(name: str) -> bool:
    pid = _read_pid(name)
    if pid is None:
        return False
    try:
        import psutil
        return psutil.pid_exists(pid) and psutil.Process(pid).status() != "zombie"
    except ImportError:
        # Fallback: send signal 0
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False


# --------------------------------------------------------------------------- #
# Core actions
# --------------------------------------------------------------------------- #

def start_service(name: str):
    if name not in SERVICES:
        print(f"[error] Unknown service: {name}")
        sys.exit(1)

    if _is_running(name):
        print(f"[{name}] Already running (PID {_read_pid(name)})")
        return

    svc = SERVICES[name]
    env = _load_env()

    log_path = svc["log"]
    log_handle = open(log_path, "a")

    proc = subprocess.Popen(
        svc["cmd"],
        cwd=svc["cwd"],
        env=env,
        stdout=log_handle,
        stderr=log_handle,
        stdin=subprocess.DEVNULL,
        start_new_session=True,  # detach from parent; no setsid needed
    )

    _write_pid(name, proc.pid)
    print(f"[{name}] Started — PID {proc.pid}  log → {log_path}")


def stop_service(name: str):
    if name not in SERVICES:
        print(f"[error] Unknown service: {name}")
        sys.exit(1)

    pid = _read_pid(name)
    if pid is None or not _is_running(name):
        print(f"[{name}] Not running.")
        _clear_pid(name)
        return

    print(f"[{name}] Stopping PID {pid}…")
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(10):
            time.sleep(0.5)
            if not _is_running(name):
                break
        else:
            os.kill(pid, signal.SIGKILL)
            print(f"[{name}] Force-killed.")
    except ProcessLookupError:
        pass

    _clear_pid(name)
    print(f"[{name}] Stopped.")


def restart_service(name: str):
    stop_service(name)
    time.sleep(1)
    start_service(name)


def status_all():
    print("\n  Agent X — Service Status")
    print("  " + "─" * 50)
    for name in SERVICES:
        running = _is_running(name)
        pid     = _read_pid(name) if running else "—"
        symbol  = "✔" if running else "✘"
        state   = "running" if running else "stopped"
        print(f"  {symbol}  {name:<22} {state:<10}  PID: {pid}")
    print()


def show_logs(name: str, lines: int = 40):
    if name not in SERVICES:
        print(f"[error] Unknown service: {name}")
        sys.exit(1)
    log_path = SERVICES[name]["log"]
    if not Path(log_path).exists():
        print(f"[{name}] No log file yet: {log_path}")
        return
    with open(log_path) as f:
        all_lines = f.readlines()
    for line in all_lines[-lines:]:
        print(line, end="")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="Agent X process manager (Termux-safe)")
    parser.add_argument(
        "action",
        choices=["start", "stop", "restart", "status", "logs"],
        help="Action to perform",
    )
    parser.add_argument(
        "service",
        nargs="?",
        default="all",
        help="Service name or 'all' (default: all)",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=40,
        help="Number of log lines to show (with 'logs' action)",
    )
    args = parser.parse_args()

    target_services = list(SERVICES.keys()) if args.service == "all" else [args.service]

    if args.action == "status":
        status_all()
        return

    if args.action == "logs":
        svc = args.service if args.service != "all" else "agent-x-core"
        show_logs(svc, args.lines)
        return

    for name in target_services:
        if args.action == "start":
            start_service(name)
        elif args.action == "stop":
            stop_service(name)
        elif args.action == "restart":
            restart_service(name)


if __name__ == "__main__":
    main()
