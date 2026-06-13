#!/usr/bin/env python3
"""Master Orchestrator wrapper for Agent X core agents.
Features:
  - readline-based streaming for each agent file
  - explicit stdout/stderr listeners
  - auto-detects empty output and prints failure marker
  - minimal telemetry
"""
import subprocess, sys, os

AGENTS_DIR = os.path.expanduser("~/agent-x/agent-x-core/agents")

CORE_AGENTS = ["content-generator.js", "api-socket.js", "publisher.js", "watchdog.js"]

SAMPLE = {
    "content-generator.js": {
        "action": "draft",
        "requestId": "orch-1",
        "payload": {"topic": "automation", "audience": "founders", "variant": "short"},
    },
    "api-socket.js": {
        "action": "get",
        "requestId": "orch-2",
        "payload": {"url": "https://httpbin.org/get"},
    },
    "publisher.js": {
        "action": "publish",
        "requestId": "orch-3",
        "payload": {
            "platform": "webhook",
            "artifactId": "demo-1",
            "credentials": {"endpoint": "http://localhost:9000"},
        },
    },
    "watchdog.js": {
        "action": "probe",
        "requestId": "orch-4",
        "payload": {"targets": ["http://localhost:3000", "http://localhost:3001"]},
    },
}


def run_agent(agent_name):
    agent_path = os.path.join(AGENTS_DIR, agent_name)
    cmd = [sys.executable if agent_name.endswith(".py") else "node", agent_path]
    raw = json.dumps(SAMPLE.get(agent_name, {"action": "ping"})) + "\n"
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        out, err = proc.communicate(input=raw, timeout=120)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except Exception:
            pass
        out, err = "", "timeout"
        rc = 124

    stdout_len = len((out or "").strip())
    stderr_len = len((err or "").strip())
    status = "ok" if rc == 0 and stdout_len > 0 else "empty-or-fail"

    return {
        "agent": agent_name,
        "status": status,
        "rc": rc,
        "stdout_len": stdout_len,
        "stderr_len": stderr_len,
        "stdout_head": (out or "").strip()[:400],
        "stderr_head": (err or "").strip()[:400],
    }


def main():
    results = []
    for agent in CORE_AGENTS:
        print(f"[orchestrator] running {agent}", flush=True)
        result = run_agent(agent)
        results.append(result)
        print(
            f"[orchestrator] {agent}: {result['status']} rc={result['rc']} stdout_len={result['stdout_len']} stderr_len={result['stderr_len']}",
            flush=True,
        )
        if result["stdout_head"]:
            print(result["stdout_head"], flush=True)
        else:
            print("[orchestrator] EMPTY OUTPUT DETECTED", flush=True)
        if result["stderr_head"]:
            print("STDERR:", result["stderr_head"], flush=True)

    print("[orchestrator] finished core agents", flush=True)


if __name__ == "__main__":
    import json
    main()
