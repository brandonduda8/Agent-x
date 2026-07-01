#!/usr/bin/env python3
"""
Agent X — Orchestrator Runner (Termux-compatible)
==================================================
Launches the JS orchestrator agent via subprocess.
Replaces any previous shell invocations that used hardcoded /usr/bin/node
or assumed systemd process management.

Usage:
    python agent-x-core/agents/orchestrator.run.py
    python agent-x-core/agents/orchestrator.run.py --task '{"type":"content","payload":{}}'
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Resolve paths using $PREFIX (Termux) or system defaults
# --------------------------------------------------------------------------- #
PREFIX   = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
REPO_DIR = Path(__file__).resolve().parent.parent.parent

# Find node — prefer $PREFIX/bin/node (Termux), fall back to PATH
import shutil as _shutil
NODE_BIN = (
    str(Path(PREFIX) / "bin" / "node")
    if Path(PREFIX, "bin", "node").exists()
    else (_shutil.which("node") or "node")
)

ORCHESTRATOR_JS = REPO_DIR / "agent-x-core" / "agents" / "orchestrator.js"
ENV_FILE        = REPO_DIR / ".env"

# --------------------------------------------------------------------------- #
# Load .env
# --------------------------------------------------------------------------- #
def load_env() -> dict:
    env = os.environ.copy()
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# --------------------------------------------------------------------------- #
# Run orchestrator
# --------------------------------------------------------------------------- #
def run(task_json: str | None = None):
    if not ORCHESTRATOR_JS.exists():
        print(f"[error] Orchestrator not found: {ORCHESTRATOR_JS}", file=sys.stderr)
        sys.exit(1)

    env = load_env()
    cmd = [NODE_BIN, str(ORCHESTRATOR_JS)]

    print(f"[orchestrator.run] Starting: {' '.join(cmd)}", flush=True)

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        env=env,
        cwd=str(REPO_DIR / "agent-x-core"),
    )

    # If a task was passed, write it to stdin and read the response
    if task_json:
        payload = task_json.encode() if isinstance(task_json, str) else task_json
        stdout_data, _ = proc.communicate(input=payload, timeout=30)
        output = stdout_data.decode().strip()
        try:
            result = json.loads(output)
            print(json.dumps(result, indent=2))
            return result
        except json.JSONDecodeError:
            print(output)
            return {"ok": False, "error": "non-JSON response", "raw": output}
    else:
        # Interactive / long-running mode
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            print("\n[orchestrator.run] Interrupted.", flush=True)

    return {"ok": True}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent X orchestrator runner")
    parser.add_argument(
        "--task",
        help='JSON task envelope, e.g. \'{"type":"content","payload":{}}\'',
        default=None,
    )
    args = parser.parse_args()

    result = run(args.task)
    if isinstance(result, dict) and not result.get("ok", True):
        sys.exit(1)
