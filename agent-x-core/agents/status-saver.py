#!/usr/bin/env python3
"""Agent: Status Saver (Python fallback)
Responsibility: Keep rated state snapshots for dashboards and audit.
Pattern: stdio JSON input/output
Bootstrap: run with python ./agents/status-saver.py
"""

import json
import os
import sys
import time
from pathlib import Path

DEFAULT_STATE_DIR = Path(os.environ.get("HOME", ".")) / "agent-x" / "state"
DEFAULT_STATE_DIR.mkdir(parents=True, exist_ok=True)


def ok(envelope):
    out = json.dumps(envelope)
    sys.stdout.write(out + "\n")
    sys.stdout.flush()


def save(status, target=None):
    target = Path(target) if target else DEFAULT_STATE_DIR / "latest.json"
    target.write_text(json.dumps(status, indent=2), encoding="utf-8")
    return str(target)


def read(target=None):
    target = Path(target) if target else DEFAULT_STATE_DIR / "latest.json"
    if not target.exists():
        return None
    return json.loads(target.read_text(encoding="utf-8"))


def run(action, payload):
    if action == "save":
        status = payload.get("status", {})
        path = save(status, payload.get("target"))
        return {"ok": True, "path": path}
    elif action == "read":
        path = payload.get("target")
        data = read(path)
        return {"ok": True, "data": data}
    elif action == "latest":
        return {"ok": True, "data": read()}
    return {"ok": False, "error": f"Unknown action: {action}"}


def main():
    buf = ""
    try:
        while True:
            chunk = sys.stdin.read(1)
            if not chunk:
                break
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if not line.strip():
                    continue
                try:
                    envelope = json.loads(line)
                except json.JSONDecodeError:
                    ok({"ok": False, "error": "Invalid JSON input"})
                    continue
                action = envelope.get("action")
                payload = envelope.get("payload") or {}
                result = run(action, payload)
                ok({"ok": True, "requestId": envelope.get("requestId"), "result": result})
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
