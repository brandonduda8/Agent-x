#!/usr/bin/env python3
"""Agent X local process manager.
- Starts/stops agent-x-core and digital-twin with auto-restart
- Writes stdout/stderr to log files under ~/agent-x/logs
- Stores PIDs under ~/agent-x/.pids
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE = Path.home() / "agent-x"
PID_DIR = BASE / ".pids"
LOG_DIR = BASE / "logs"
STATE_FILE = BASE / ".process-manager-state.json"

for d in [PID_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SERVICES = {
    "agent-x-core": {
        "cwd": BASE / "agent-x-core",
        "cmd": ["node", "index.js"],
        "env": {"NODE_ENV": "production"},
    },
    "digital-twin": {
        "cwd": BASE / "digital-twin",
        "cmd": ["node", "index.js"],
        "env": {"NODE_ENV": "production"},
    },
}


def pid_path(name):
    return PID_DIR / f"{name}.pid"


def log_path(name):
    return LOG_DIR / f"{name}.log"


def read_pid(name):
    p = pid_path(name)
    if not p.exists():
        return None
    try:
        return int(p.read_text().strip())
    except ValueError:
        return None


def write_pid(name, pid):
    pid_path(name).write_text(str(pid))


def remove_pid(name):
    try:
        pid_path(name).unlink()
    except FileNotFoundError:
        pass


def is_running(pid):
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def start_service(name):
    cfg = SERVICES[name]
    existing = read_pid(name)
    if existing and is_running(existing):
        return {"ok": True, "status": "already-running", "pid": existing}

    log_file = log_path(name).open("a")
    proc = subprocess.Popen(
        cfg["cmd"],
        cwd=str(cfg["cwd"]),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        env={**os.environ, **cfg.get("env", {})},
        close_fds=True,
    )
    write_pid(name, proc.pid)
    time.sleep(1.5)
    if is_running(proc.pid):
        return {"ok": True, "status": "started", "pid": proc.pid}
    else:
        remove_pid(name)
        return {"ok": False, "status": "failed-to-start", "pid": proc.pid}


def stop_service(name):
    pid = read_pid(name)
    if not pid or not is_running(pid):
        remove_pid(name)
        return {"ok": True, "status": "not-running"}
    try:
        os.kill(pid, 15)  # SIGTERM
        time.sleep(1)
        if is_running(pid):
            os.kill(pid, 9)  # SIGKILL
            time.sleep(0.5)
    except ProcessLookupError:
        pass
    remove_pid(name)
    return {"ok": True, "status": "stopped"}


def status_all():
    out = {}
    for name in SERVICES:
        pid = read_pid(name)
        out[name] = {
            "pid": pid,
            "running": is_running(pid),
            "pid_file": str(pid_path(name)),
            "log_file": str(log_path(name)),
        }
    return out


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: process-manager.py <start|stop|restart|status> [service]"}, indent=2))
        raise SystemExit(1)

    action = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else None

    if action == "start":
        if target:
            print(json.dumps(start_service(target), indent=2))
        else:
            results = {}
            for name in SERVICES:
                results[name] = start_service(name)
            print(json.dumps(results, indent=2))
    elif action == "stop":
        if target:
            print(json.dumps(stop_service(target), indent=2))
        else:
            results = {}
            for name in SERVICES:
                results[name] = stop_service(name)
            print(json.dumps(results, indent=2))
    elif action == "restart":
        if target:
            stop_service(target)
            time.sleep(1)
            print(json.dumps(start_service(target), indent=2))
        else:
            for name in SERVICES:
                stop_service(name)
                time.sleep(1)
                start_service(name)
            print(json.dumps(status_all(), indent=2))
    elif action == "status":
        print(json.dumps(status_all(), indent=2))
    else:
        print(json.dumps({"error": f"unknown action: {action}"}, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
