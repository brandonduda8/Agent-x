#!/usr/bin/env python3
"""
Agent X — Status CLI Viewer (Termux-compatible)
================================================
Terminal-based status display.  Replaces any previous version that called
`systemctl` or assumed /var/run paths.

Usage:
    python agent-x-core/agents/Status.cli.py
    python agent-x-core/agents/Status.cli.py --watch       # refresh every 5 s
    python agent-x-core/agents/Status.cli.py --watch --interval 10
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

# Add repo root so we can import status-saver helpers
sys.path.insert(0, str(REPO_DIR / "agent-x-core" / "agents"))

# --------------------------------------------------------------------------- #
# ANSI colours (always safe — Termux terminal supports them)
# --------------------------------------------------------------------------- #
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[0;32m"
RED    = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN   = "\033[0;36m"
DIM    = "\033[2m"


def _clear():
    os.system("clear")


def _fmt_service(name: str, info: dict) -> str:
    status = info.get("status", "unknown")
    pid    = info.get("pid", "—")
    restarts = info.get("restarts", "")

    if status == "online" or status == "running":
        sym   = f"{GREEN}✔{RESET}"
        label = f"{GREEN}{status}{RESET}"
    elif status == "stopped":
        sym   = f"{RED}✘{RESET}"
        label = f"{RED}{status}{RESET}"
    elif status == "errored":
        sym   = f"{RED}✘{RESET}"
        label = f"{RED}{status}{RESET}"
    else:
        sym   = f"{YELLOW}~{RESET}"
        label = f"{YELLOW}{status}{RESET}"

    restart_str = f"  restarts: {restarts}" if restarts else ""
    return f"  {sym}  {name:<22} {label:<20}  pid: {pid}{restart_str}"


def _load_state() -> dict:
    state_file = REPO_DIR / "memory" / "state.json"
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _load_tasks() -> list:
    for p in [
        REPO_DIR / "memory" / "tasks.json",
        REPO_DIR / "data" / "tasks.json",
    ]:
        if p.exists():
            try:
                data = json.loads(p.read_text())
                return data if isinstance(data, list) else []
            except Exception:
                pass
    return []


def _run_status_saver() -> dict:
    """Invoke status-saver.py and return the parsed dict."""
    script = REPO_DIR / "agent-x-core" / "agents" / "status-saver.py"
    if not script.exists():
        return {}
    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            timeout=10,
        )
        lines = result.stdout.decode().splitlines()
        # status-saver prints one line of prose then a JSON block
        json_lines = [l for l in lines if l.strip().startswith("{")]
        if json_lines:
            return json.loads("\n".join(json_lines))
    except Exception:
        pass
    return {}


def display(data: dict):
    services = data.get("services", {})
    ts       = data.get("timestamp", 0)
    source   = data.get("source", "unknown")
    tasks    = _load_tasks()
    state    = _load_state()

    pending   = sum(1 for t in tasks if t.get("status") == "pending")
    running_t = sum(1 for t in tasks if t.get("status") == "running")
    done      = sum(1 for t in tasks if t.get("status") == "done")

    print()
    print(f"{BOLD}{CYAN}══════════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN}           Agent X — Status               {RESET}")
    print(f"{BOLD}{CYAN}══════════════════════════════════════════{RESET}")
    print(f"{DIM}  Updated : {time.strftime('%H:%M:%S', time.localtime(ts)) if ts else 'N/A'}"
          f"   source: {source}{RESET}")
    print()

    print(f"{BOLD}  Services:{RESET}")
    for name, info in services.items():
        print(_fmt_service(name, info))
    print()

    print(f"{BOLD}  Tasks:{RESET}")
    print(f"    Total    : {len(tasks)}")
    print(f"    Pending  : {YELLOW}{pending}{RESET}")
    print(f"    Running  : {CYAN}{running_t}{RESET}")
    print(f"    Done     : {GREEN}{done}{RESET}")
    print()

    revenue = state.get("revenue", data.get("revenue", 0))
    if revenue:
        print(f"{BOLD}  Revenue:{RESET}  ${revenue:,.2f}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Agent X status CLI")
    parser.add_argument("--watch",    action="store_true", help="Refresh continuously")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds")
    args = parser.parse_args()

    if args.watch:
        while True:
            _clear()
            data = _run_status_saver()
            display(data)
            print(f"{DIM}  [watch mode — refreshing every {args.interval}s  Ctrl-C to quit]{RESET}")
            time.sleep(args.interval)
    else:
        data = _run_status_saver()
        display(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
