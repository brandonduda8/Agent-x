#!/usr/bin/env python3
"""Utility: inspect, create, or show next missing pieces of the agent-x framework.
Run with: python Status.show.py
"""

import os
import json


BASE = os.path.expanduser("~/agent-x")
PATHS = {
    "core": os.path.join(BASE, "agent-x-core", "index.js"),
    "twin": os.path.join(BASE, "digital-twin", "index.js"),
    "agents_api_socket": os.path.join(BASE, "agent-x-core", "agents", "api-socket.js"),
    "agents_content_generator": os.path.join(BASE, "agent-x-core", "agents", "content-generator.js"),
    "agents_data_aggregator": os.path.join(BASE, "agent-x-core", "agents", "data-aggregator.js"),
    "agents_infrastructure": os.path.join(BASE, "agent-x-core", "agents", "infrastructure.js"),
    "agents_watchdog": os.path.join(BASE, "agent-x-core", "agents", "watchdog.js"),
    "agents_orchestrator": os.path.join(BASE, "agent-x-core", "agents", "orchestrator.js"),
    "agents_publisher": os.path.join(BASE, "agent-x-core", "agents", "publisher.js"),
    "agents_status_saver": os.path.join(BASE, "agent-x-core", "agents", "status-saver.py"),
    "communication_packet_schema": os.path.join(BASE, "communication", "packet-schema.js"),
    "deployment_termux_boot": os.path.join(BASE, "deployment", "termux-boot.sh"),
    "deployment_agent_x_core_service": os.path.join(BASE, "deployment", "agent-x-core.service"),
    "deployment_digital_twin_service": os.path.join(BASE, "deployment", "digital-twin.service"),
}


def check_state():
    return {
        name: {
            "exists": os.path.exists(path),
            "mtime": os.path.getmtime(path) if os.path.exists(path) else None,
        }
        for name, path in PATHS.items()
    }


def missing(state):
    return [name for name, info in state.items() if not info["exists"]]


def main():
    state = check_state()
    data = {
        "status.runtime": {
            "node": os.popen("node -v").read().strip(),
            "python": os.popen("python -V").read().strip(),
        },
        "status.framework": {
            "missing": missing(state),
            "state": state,
        },
        "status.next": [
            [
                "publisher-run",
                "Run the publisher agent now",
                "cd ~/agent-x/agent-x-core/agents && printf '%s' '{\"action\":\"publish\",\"requestId\":\"demo1\",\"payload\":{\"platform\":\"webhook\",\"credentials\":{\"endpoint\":\"http://localhost:9000\"},\"artifactId\":\"<artifact file stem>\"}}' | node publisher.js",
            ]
        ],
    }
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
