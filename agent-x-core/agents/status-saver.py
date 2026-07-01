#!/usr/bin/env python3
"""
Agent X — Status Saver (Termux-compatible)
==========================================
Reads current PM2 / process state and writes a structured JSON snapshot
to memory/state.json.  Replaces any previous version that called
`systemctl status` or assumed /var/run paths.

Usage:
    python agent-x-core/agents/status-saver.py
    python agent-x-core/agents/status-saver.py --out /path/to/state.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
PREFIX   = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
REPO_DIR = Path(__file__).resolve().parent.parent.parent
STATE_FILE_DEFAULT = REPO_DIR / "memory" / "state.json"
PID_DIR  = REPO_DIR / "logs" / "pids"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

SERVICES = ["agent-x-core", "digital-twin", "dashboard", "webhook-listener"]


def _pm2_available() -> bool:
    import shutil
    return shutil.which("pm2") is not None


def _pm2_status() -> dict:
    """Return a dict of service_name → pm2 status info."""
    try:
        result = subprocess.run(
            ["pm2", "jlist"],
            capture_output=True,
            timeout=10,
        )
        processes = json.loads(result.stdout.decode())
        out = {}
        for proc in processes:
            name   = proc.get("name", "unknown")
            status = proc.get("pm2_env", {}).get("status", "unknown")
            pid    = proc.get("pid")
            restarts = proc.get("pm2_env", {}).get("restart_time", 0)
            out[name] = {"status": status, "pid": pid, "restarts": restarts}
        return out
    except Exception:
        return {}


def _pid_file_status() -> dict:
    """Fallback: read PID files written by process-manager.py."""
    out = {}
    if not PID_DIR.exists():
        return out

    import shutil
    for name in SERVICES:
        pf = PID_DIR / f"{name}.pid"
        if pf.exists():
            try:
                pid = int(pf.read_text().strip())
                # Check if still alive
                try:
                    os.kill(pid, 0)
                    out[name] = {"status": "running", "pid": pid}
                except (ProcessLookupError, PermissionError):
                    out[name] = {"status": "stopped", "pid": None}
            except ValueError:
                out[name] = {"status": "unknown", "pid": None}
        else:
            out[name] = {"status": "stopped", "pid": None}
    return out


def _memory_state() -> dict:
    """Read memory/state.json for last-known agent state."""
    state_file = REPO_DIR / "memory" / "state.json"
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _task_count() -> int:
    tasks_file = REPO_DIR / "memory" / "tasks.json"
    if tasks_file.exists():
        try:
            tasks = json.loads(tasks_file.read_text())
            return len(tasks) if isinstance(tasks, list) else 0
        except Exception:
            pass
    return 0


def collect_status() -> dict:
    if _pm2_available():
        services = _pm2_status()
        source = "pm2"
    else:
        services = _pid_file_status()
        source = "pid-files"

    # Fill in any missing service entries as stopped
    for name in SERVICES:
        if name not in services:
            services[name] = {"status": "stopped", "pid": None}

    memory_state = _memory_state()

    return {
        "timestamp": int(time.time()),
        "source":    source,
        "services":  services,
        "tasks": {
            "total": _task_count(),
        },
        "agents": memory_state.get("agents", {}),
        "revenue": memory_state.get("revenue", 0),
    }


def save_status(out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    status = collect_status()
    out_path.write_text(json.dumps(status, indent=2))
    print(f"[status-saver] State written to {out_path}")
    return status


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent X status saver")
    parser.add_argument(
        "--out",
        default=str(STATE_FILE_DEFAULT),
        help=f"Output path (default: {STATE_FILE_DEFAULT})",
    )
    args = parser.parse_args()

    status = save_status(Path(args.out))
    print(json.dumps(status, indent=2))
