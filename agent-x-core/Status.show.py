#!/usr/bin/env python3
"""
Agent X — Status Show Utility (Termux-compatible)
=================================================
Pretty-prints the current memory/state.json and PM2 process table.
Replaces any previous version that used `systemctl` or hardcoded paths.

Usage:
    python agent-x-core/Status.show.py
    python agent-x-core/Status.show.py --json     # raw JSON output
    python agent-x-core/Status.show.py --services # services only
    python agent-x-core/Status.show.py --tasks    # tasks only
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PREFIX   = os.environ.get("PREFIX", "/data/data/com.termux/files/usr}")
REPO_DIR = Path(__file__).resolve().parent.parent

BOLD  = "\033[1m"
GREEN = "\033[0;32m"
RED   = "\033[0;31m"
CYAN  = "\033[0;36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return default


def _pm2_list() -> list:
    import shutil
    if not shutil.which("pm2"):
        return []
    try:
        r = subprocess.run(["pm2", "jlist"], capture_output=True, timeout=8)
        return json.loads(r.stdout.decode())
    except Exception:
        return []


def show_services(pm2_procs: list):
    print(f"\n{BOLD}Services (PM2):{RESET}")
    if not pm2_procs:
        print(f"  {DIM}(no PM2 processes — is PM2 running?){RESET}")
        return
    for p in pm2_procs:
        name   = p.get("name", "?")
        status = p.get("pm2_env", {}).get("status", "?")
        pid    = p.get("pid", "—")
        sym    = f"{GREEN}✔{RESET}" if status == "online" else f"{RED}✘{RESET}"
        print(f"  {sym}  {name:<24} {status:<12}  pid {pid}")


def show_tasks(tasks: list):
    print(f"\n{BOLD}Tasks ({len(tasks)}):{RESET}")
    if not tasks:
        print(f"  {DIM}(none){RESET}")
        return
    for t in tasks[:20]:  # cap at 20 for readability
        tid    = t.get("id", t.get("requestId", "?"))[:16]
        ttype  = t.get("type", t.get("action", "?"))
        status = t.get("status", "?")
        if status == "done":
            sym = f"{GREEN}✔{RESET}"
        elif status == "running":
            sym = f"{CYAN}►{RESET}"
        else:
            sym = "○"
        print(f"  {sym}  {tid:<18}  {ttype:<22}  {status}")
    if len(tasks) > 20:
        print(f"  {DIM}… and {len(tasks)-20} more{RESET}")


def show_state(state: dict):
    print(f"\n{BOLD}System State:{RESET}")
    ts = state.get("timestamp", state.get("updated_at"))
    if ts:
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts)))
        print(f"  Updated   : {ts_str}")
    revenue = state.get("revenue", 0)
    if revenue:
        print(f"  Revenue   : ${revenue:,.2f}")
    agents = state.get("agents", {})
    if agents:
        print(f"  Agents    : {', '.join(agents.keys())}")


def main():
    parser = argparse.ArgumentParser(description="Agent X status display")
    parser.add_argument("--json",     action="store_true", help="Print raw JSON")
    parser.add_argument("--services", action="store_true", help="Show services only")
    parser.add_argument("--tasks",    action="store_true", help="Show tasks only")
    args = parser.parse_args()

    state  = _load_json(REPO_DIR / "memory" / "state.json",  {})
    tasks  = _load_json(REPO_DIR / "memory" / "tasks.json",  [])
    if not isinstance(tasks, list):
        tasks = []
    pm2_procs = _pm2_list()

    if args.json:
        print(json.dumps({"state": state, "tasks": tasks, "pm2": pm2_procs}, indent=2))
        return

    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN}        Agent X — Status Report        {RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")

    if args.services:
        show_services(pm2_procs)
    elif args.tasks:
        show_tasks(tasks)
    else:
        show_state(state)
        show_services(pm2_procs)
        show_tasks(tasks)
    print()


if __name__ == "__main__":
    main()
