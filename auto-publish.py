#!/usr/bin/env python3

import json
import os
import time
import urllib.request
from pathlib import Path

BASE = Path.home() / "agent-x"

TWIN_URL = os.environ.get("DIGITAL_TWIN_URL", "http://localhost:3001")
SINK_URL = os.environ.get("PUBLISH_SINK_URL", "http://localhost:3002")

GENERATED = BASE / "generated"
GENERATED.mkdir(parents=True, exist_ok=True)


def schedule_human(title, audience, variant):
    return {
        "topic": f"{title} for {audience}",
        "audience": audience,
        "variation": variant,
        "tags": [audience.lower().replace(" ", "_"), variant.lower().replace(" ", "_")],
    }


def twin_execute(payload):
    url = f"{TWIN_URL}/execute"
    body = json.dumps({"type": "content-generation", "payload": payload}).encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def deliver_to_sink(payload, twin_result):
    data = {
        "source": "agent-x-auto-publish",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "payload": payload,
        "twin": twin_result
    }

    req = urllib.request.Request(
        SINK_URL,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def main():
    title = os.environ.get("AGENTX_AUTO_TITLE", "Ad creatives that convert")
    audience = os.environ.get("AGENTX_AUTO_AUDIENCE", "performance marketers")
    variant = os.environ.get("AGENTX_AUTO_VARIANT", "launch campaign")

    payload = schedule_human(title, audience, variant)

    twin_result = twin_execute(payload)

    delivery = deliver_to_sink(payload, twin_result)

    log_file = GENERATED / f"run_{int(time.time())}.json"
    log_file.write_text(json.dumps({
        "payload": payload,
        "twin": twin_result,
        "delivery": delivery
    }, indent=2))

    print(json.dumps({
        "ok": True,
        "delivery": delivery,
        "log": str(log_file)
    }))


if __name__ == "__main__":
    main()
