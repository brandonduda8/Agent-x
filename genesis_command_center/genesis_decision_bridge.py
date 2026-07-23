import json
from datetime import datetime


decisions = [

    {
        "priority": 1,
        "decision": "Secure income first",
        "category": "income",
        "agent": "Opportunity Discovery Agent",
        "action": "Review highest probability opportunities",
        "approval_required": True
    },

    {
        "priority": 2,
        "decision": "Build revenue pipeline",
        "category": "revenue",
        "agent": "Revenue Agent",
        "action": "Prepare approved outreach campaign",
        "approval_required": True
    },

    {
        "priority": 3,
        "decision": "Expand Genesis automation",
        "category": "technology",
        "agent": "Technology Agent",
        "action": "Improve adapters",
        "approval_required": False
    }

]


dispatches = []


for decision in decisions:

    dispatches.append({

        "mission":
            decision["decision"],

        "assigned_agent":
            decision["agent"],

        "action":
            decision["action"],

        "approval_required":
            decision["approval_required"],

        "status":
            "DISPATCHED",

        "timestamp":
            str(datetime.now())

    })


output = {

    "system":
        "GENESIS DECISION BRIDGE",

    "status":
        "ONLINE",

    "timestamp":
        str(datetime.now()),

    "decisions_received":
        len(decisions),

    "missions_dispatched":
        dispatches

}


print(json.dumps(output, indent=4))
