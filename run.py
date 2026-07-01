#!/usr/bin/env python3
"""
Agent X — Python Launch Script (Termux-compatible)
===================================================
Convenience entry point for starting Agent X from Python.
Delegates to process-manager.py for actual process control.

Usage:
    python run.py            # start all services
    python run.py core       # start agent-x-core only
    python run.py status     # show process status
    python run.py stop       # stop all services
"""

import os
import sys
import subprocess
from pathlib import Path

REPO_DIR   = Path(__file__).resolve().parent
MANAGER    = REPO_DIR / "process-manager.py"
PYTHON_BIN = sys.executable

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "start"

    # Map shorthand aliases
    action_map = {
        "start":   ["start",   "all"],
        "stop":    ["stop",    "all"],
        "restart": ["restart", "all"],
        "status":  ["status"],
        "core":    ["start",   "agent-x-core"],
        "twin":    ["start",   "digital-twin"],
        "dashboard": ["start", "dashboard"],
        "webhook": ["start",   "webhook-listener"],
    }

    if arg not in action_map:
        print(f"Usage: python run.py [start|stop|restart|status|core|twin|dashboard|webhook]")
        sys.exit(1)

    cmd = [PYTHON_BIN, str(MANAGER)] + action_map[arg]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
