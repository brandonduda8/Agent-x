import json
import os
from datetime import datetime


VAULT = "opportunities.json"


def load():

    if os.path.exists(VAULT):

        with open(VAULT, "r") as f:
            return json.load(f)

    return []


opportunities = load()


response = {

    "system": "GENESIS OPPORTUNITY COMMAND CENTER",

    "timestamp": str(datetime.now()),

    "commands": {

        "/opportunities":
        "View ranked opportunities",

        "/nextmove":
        "Show highest priority action",

        "/approve ID":
        "Approve opportunity action",

        "/deny ID":
        "Reject opportunity action"

    },


    "current_opportunities": []

}


for item in opportunities:

    response["current_opportunities"].append({

        "id": item["id"],

        "category": item["category"],

        "title": item["title"],

        "priority": item["priority"],

        "status": item["status"],

        "approval_required":
        item.get("approval_required", False)

    })


print(json.dumps(response, indent=4))
