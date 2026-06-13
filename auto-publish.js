#!/usr/bin/env python3
"""Agent X auto-publish pipeline: generate content and publish to Webhook sink.

Outputs:
- local JSON task output in generated/task_log_*
- prints a lightweight delivery receipt
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path.home() / "agent-x"
TWIN = BASE / "digital-twin"
TWIN_URL = os.environ.get("DIGITAL_TWIN_URL", "http://localhost:3001")
SINK_URL = os.environ.get("PUBLISH_SINK_URL", "http://localhost:4000/ingest")

GENERATED = BASE / "generated"
GENERATED.mkdir(parents=True, exist_ok=True)

def schedule_human(title, audience, cta_or_variant):
  topic = f"{title} for {audience}"
  tags = [audience.lower().replace(" ","_"), cta_or_variant.lower().replace(" ","_")]
  return {
    "topic": topic,
    "audience": audience,
    "variation": cta_or_variant,
    "tags": tags,
    "channels": ["newsletter", "blog", "social_draft"],
    "cta": cta_or_variant,
  }

def execute_type_factory(payload):
  return {
    "type": "content-generation",
    "payload": payload,
    "createdById": "auto",
    "priority": "normal",
  }

def deliver_to_sink(task, receipt):
  data = json.dumps({
    "source": "agent-x-auto-publish",
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "task": task,
    "deliveryReceipt": receipt,
  })
  req = urllib.request.Request(
    SINK_URL,
    data=data.encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
  )
  try:
    with urllib.request.urlopen(req, timeout=20) as r:
      return {"httpCode": r.status, "body": json.loads(r.read().decode("utf-8", errors="ignore"))}
  except Exception as e:
    return {"httpCode": None, "error": str(e)}

def main():
  title = os.environ.get("AGENTX_AUTO_TITLE", "Ad creatives that convert")
  audience = os.environ.get("AGENTX_AUTO_AUDIENCE", "performance marketers")
  variant = os.environ.get("AGENTX_AUTO_VARIANT", "launch campaign")
  payload = schedule_human(title, audience, variant)
  task = execute_type_factory(payload)

  task_id = None
  try:
    url = f"{TWIN_URL}/execute"
    req = urllib.request.Request(
      url,
      data=json.dumps({"taskId": None, "type": task["type"], "payload": task["payload"]}).encode("utf-8"),
      headers={"Content-Type": "application/json", "X-Request-Id": "auto-" + str(int(time.time()*1000))},
      method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
      body = json.loads(r.read().decode())
      task_id = body.get("taskId")

    artifact_slug = task_id or f"local-{int(time.time()*1000)}"
    log_path = GENERATED / f"task_log_{artifact_slug}.json"
    output = {
      "runAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
      "taskId": task_id,
      "twinResponse": body,
      "delivery": None,
    }
    if task_id:
      receipt = deliver_to_sink(task, body)
      output["delivery"] = receipt

    log_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(json.dumps({
      "ok": True,
      "taskId": task_id,
      "delivery": output.get("delivery"),
      "log": str(log_path),
    }))
  except Exception as e:
    print(json.dumps({"ok": False, "error": str(e)}))
    raise

if __name__ == "__main__":
  main()
