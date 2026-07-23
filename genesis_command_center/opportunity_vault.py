import json
import os
from datetime import datetime


FILE = "opportunities.json"


def load():

    if os.path.exists(FILE):

        with open(FILE, "r") as f:
            return json.load(f)

    return []


def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


opportunities = load()


new_entry = {

    "id": len(opportunities) + 1,

    "category": "business",

    "title": "Example Opportunity",

    "description":
    "Potential income or business opportunity",

    "priority":
    "HIGH",

    "status":
    "NEW",

    "next_action":
    "Review and decide",

    "created":
    str(datetime.now())

}


if not opportunities:

    opportunities.append(new_entry)

    save(opportunities)


output = {

    "system":
    "GENESIS OPPORTUNITY VAULT",

    "status":
    "ONLINE",

    "timestamp":
    str(datetime.now()),

    "total_opportunities":
    len(opportunities),

    "opportunities":
    opportunities

}


print(json.dumps(output, indent=4))
