#!/usr/bin/env python3
"""Minimal wrapper to run one js agent and capture exact stdout/stderr."""
import subprocess, sys, json, os

agent = os.path.join(os.path.expanduser("~"), "agent-x", "agent-x-core", "agents", "content-generator.js")
payload = json.dumps({"action":"draft","requestId":"final1","payload":{"topic":"automation","audience":"founders","variant":"short"}}) + "\n"
p = subprocess.run(["node", agent], input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("rc=", p.returncode)
print("stdout_len=", len(p.stdout or ""))
print("stderr_len=", len(p.stderr or ""))
print("stdout=", repr((p.stdout or "").strip()))
print("stderr=", repr((p.stderr or "").strip()[:500]))
