import json
import os
from datetime import datetime


VAULT = "opportunities.json"


def load():

    if os.path.exists(VAULT):

        with open(VAULT, "r") as f:
            return json.load(f)

    return []


def save(data):

    with open(VAULT, "w") as f:
        json.dump(data, f, indent=4)


opportunities = load()


incoming = [

    {
        "source_agent": "Opportunity Discovery Agent",
        "category": "income",
        "title": "High probability employment opportunity",
        "description": "Potential job match requiring review",
        "priority": "HIGH"
    },

    {
        "source_agent": "Revenue Agent",
        "category": "business",
        "title": "Potential client opportunity",
        "description": "Business outreach candidate requiring approval",
        "priority": "HIGH"
    }

]


created = []


for item in incoming:

    entry = {

        "id": len(opportunities) + 1,

        "category": item["category"],

        "title": item["title"],

        "description": item["description"],

        "source_agent": item["source_agent"],

        "priority": item["priority"],

        "status": "NEW",

        "approval_required": True,

        "next_action": "Review by operator",

        "created": str(datetime.now())

    }

    opportunities.append(entry)

    created.append(entry)


save(opportunities)


print(json.dumps({

    "system": "GENESIS OPPORTUNITY INTAKE BRIDGE",

    "status": "ONLINE",

    "timestamp": str(datetime.now()),

    "new_opportunities_added": len(created),

    "entries": created

}, indent=4))
