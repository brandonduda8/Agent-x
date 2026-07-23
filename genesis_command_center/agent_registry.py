import json
from datetime import datetime


registry = {
    "system": "GENESIS AGENT REGISTRY",
    "timestamp": str(datetime.now()),

    "agents": [
        {
            "name": "Genesis Core",
            "role": "Orchestrator",
            "status": "ONLINE"
        },
        {
            "name": "Hermes Agent",
            "role": "Communication Intelligence",
            "status": "ONLINE"
        },
        {
            "name": "Revenue Agent",
            "role": "Business Development",
            "status": "ONLINE"
        },
        {
            "name": "Opportunity Discovery Agent",
            "role": "Income Discovery",
            "status": "ONLINE"
        },
        {
            "name": "Stability Agent",
            "role": "Housing Resources",
            "status": "ONLINE"
        },
        {
            "name": "Technology Agent",
            "role": "Automation Engineering",
            "status": "ONLINE"
        }
    ],

    "adapters": [
        {
            "name": "Phone Adapter",
            "endpoint": "android-termux",
            "status": "ONLINE"
        },
        {
            "name": "Telegram Adapter",
            "endpoint": "telegram_gateway",
            "status": "ONLINE"
        },
        {
            "name": "CRM Adapter",
            "endpoint": "crm_memory",
            "status": "ONLINE"
        },
        {
            "name": "Approval Adapter",
            "endpoint": "approval_engine",
            "status": "ONLINE"
        },
        {
            "name": "OpenClaw Adapter",
            "endpoint": "openclaw_bridge",
            "status": "READY"
        },
        {
            "name": "Agent Harness Adapter",
            "endpoint": "agent_harness",
            "status": "ONLINE"
        }
    ],

    "external_systems": [
        {
            "name": "OpenClaw",
            "status": "READY_FOR_BRIDGE"
        },
        {
            "name": "Hermes",
            "status": "CONNECTED"
        },
        {
            "name": "Origami",
            "status": "READY_FOR_ADAPTER"
        },
        {
            "name": "Agent X",
            "status": "READY_FOR_ADAPTER"
        },
        {
            "name": "Agent JSON",
            "status": "READY_FOR_ADAPTER"
        }
    ]
}


print(json.dumps(registry, indent=4))
