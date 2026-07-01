#!/usr/bin/env python3
"""
Agent X — Single Agent Launcher (Termux-compatible)
=====================================================
Runs one stdio-JSON worker agent, sends it a single request, and prints
the response.  Useful for testing and one-shot task execution.

Previously used hardcoded /usr/local/bin/node — now resolved via $PREFIX.

Usage:
    python agent-x-core/agents/run_one.py <agent> <action> [payload_json]

Examples:
    python agent-x-core/agents/run_one.py api-socket get '{"url":"https://httpbin.org/get"}'
    python agent-x-core/agents/run_one.py content-generator draft '{"topic":"automation","audience":"founders","variant":"short"}'
    python agent-x-core/agents/run_one.py data-aggregator aggregate '{"sourceUrls":["https://example.com"],"timeWindow":"24h"}'
"""

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

# --------------------------------------------------------------------------- #
# Resolve node binary path
# --------------------------------------------------------------------------- #
PREFIX   = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
REPO_DIR = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = REPO_DIR / "agent-x-core" / "agents"

import shutil as _shutil
NODE_BIN = (
    str(Path(PREFIX) / "bin" / "node")
    if Path(PREFIX, "bin", "node").exists()
    else (_shutil.which("node") or "node")
)

KNOWN_AGENTS = {
    "api-socket":        "api-socket.js",
    "content-generator": "content-generator.js",
    "data-aggregator":   "data-aggregator.js",
    "infrastructure":    "infrastructure.js",
    "publisher":         "publisher.js",
    "watchdog":          "watchdog.js",
    "orchestrator":      "orchestrator.js",
}


def run_agent(agent_name: str, action: str, payload: dict) -> dict:
    """Send one JSON request to a stdio agent and return parsed response."""

    js_file = KNOWN_AGENTS.get(agent_name)
    if js_file is None:
        return {"ok": False, "error": f"Unknown agent '{agent_name}'. Known: {list(KNOWN_AGENTS)}"}

    agent_path = AGENTS_DIR / js_file
    if not agent_path.exists():
        return {"ok": False, "error": f"Agent file not found: {agent_path}"}

    request = {
        "action":    action,
        "requestId": str(uuid.uuid4()),
        "payload":   payload,
    }
    request_json = json.dumps(request).encode()

    env = os.environ.copy()
    env_file = REPO_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")

    try:
        result = subprocess.run(
            [NODE_BIN, str(agent_path)],
            input=request_json,
            capture_output=True,
            timeout=30,
            env=env,
            cwd=str(AGENTS_DIR),
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Agent timed out after 30 seconds"}
    except FileNotFoundError:
        return {"ok": False, "error": f"node not found at: {NODE_BIN}"}

    stdout = result.stdout.decode().strip()
    stderr = result.stderr.decode().strip()

    if stderr:
        print(f"[stderr] {stderr}", file=sys.stderr)

    if not stdout:
        return {"ok": False, "error": "Agent produced no output", "exit_code": result.returncode}

    # The agent may emit multiple lines; take the last valid JSON line
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue

    return {"ok": False, "error": "No valid JSON in agent output", "raw": stdout}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    agent_name = sys.argv[1]
    action     = sys.argv[2]
    payload_raw = sys.argv[3] if len(sys.argv) > 3 else "{}"

    try:
        payload = json.loads(payload_raw)
    except json.JSONDecodeError as e:
        print(f"[error] Invalid JSON payload: {e}", file=sys.stderr)
        sys.exit(1)

    response = run_agent(agent_name, action, payload)
    print(json.dumps(response, indent=2))

    if not response.get("ok", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
