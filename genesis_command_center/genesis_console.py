import json
import os
from datetime import datetime


def exists(file):
    return os.path.exists(file)


def load_json(file):
    if exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


profile = load_json("profile.json")


console = {
    "system": "GENESIS OPERATOR CONSOLE",

    "timestamp": str(datetime.now()),

    "operator": profile.get(
        "operator",
        "Brandon Duda"
    ),

    "system_status": {
        "core": "ONLINE",
        "agents": "SYNCHRONIZED",
        "adapters": "CONNECTED",
        "models": "READY",
        "memory": "ACTIVE"
    },

    "mission_control": [
        {
            "priority": 1,
            "mission": "Secure income",
            "agent": "Opportunity Discovery Agent",
            "action": "Review highest-value opportunities"
        },
        {
            "priority": 2,
            "mission": "Build revenue pipeline",
            "agent": "Revenue Agent",
            "action": "Review leads and prepare outreach"
        },
        {
            "priority": 3,
            "mission": "Improve Genesis",
            "agent": "Technology Agent",
            "action": "Expand automation"
        }
    ],

    "approval_center": {
        "status": "READY",
        "policy": "External actions require operator approval"
    },

    "connected_assets": {
        "profile": exists("profile.json"),
        "opportunity_vault": exists("opportunities.json"),
        "performance_memory": exists(
            "genesis_performance_memory.json"
        )
    },

    "available_commands": [
        "/status",
        "/brief",
        "/opportunities",
        "/nextmove",
        "/approve ID",
        "/deny ID"
    ]
}


print(
    json.dumps(
        console,
        indent=4
    )
)
