import json
import os
from datetime import datetime


def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except:
            return default
    return default


profile = load_json(
    "vault_profile.json",
    {
        "operator_profile": {
            "name": "Genesis Operator"
        }
    }
)


state = load_json(
    "memory.json",
    {}
)


audit = load_json(
    "genesis_audit_log.json",
    []
)


brief = {

    "system": "GENESIS DAILY COMMAND CENTER",

    "timestamp": str(datetime.now()),


    "operator": {

        "name":
        profile.get("operator_profile", {}).get(
            "name",
            "Unknown"
        ),

        "status":
        "ONLINE"

    },


    "system_health": {

        "core":
        "ONLINE",

        "agents":
        "SYNCHRONIZED",

        "adapters":
        "CONNECTED",

        "memory":
        "ACTIVE"

    },


    "daily_priorities": [

        {
            "priority": 1,

            "mission":
            "Secure income",

            "agent":
            "Opportunity Discovery Agent",

            "next_action":
            "Review highest probability opportunities"

        },


        {
            "priority": 2,

            "mission":
            "Build revenue pipeline",

            "agent":
            "Revenue Agent",

            "next_action":
            "Review leads and prepare approved outreach"

        },


        {
            "priority": 3,

            "mission":
            "Technology growth",

            "agent":
            "Technology Agent",

            "next_action":
            "Improve Genesis automation"

        }

    ],


    "approval_center": {

        "status":
        "READY",

        "policy":
        "External actions require operator approval"

    },


    "memory_status": {

        "events_recorded":
        len(audit),

        "state":
        "ACTIVE"

    },


    "next_power_move":

    "Complete highest-value income action first"

}


print(json.dumps(brief, indent=4))
