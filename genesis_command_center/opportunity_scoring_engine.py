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


ranked = []


for item in opportunities:

    score = 0


    if item.get("priority") == "HIGH":
        score += 40

    if item.get("category") == "business":
        score += 30

    if item.get("status") == "NEW":
        score += 20


    score += 10


    ranked.append({

        "id": item["id"],

        "title": item["title"],

        "category": item["category"],

        "score": score,

        "recommendation":
        "Review highest-value opportunity first",

        "approval_required":
        True

    })


ranked.sort(
    key=lambda x: x["score"],
    reverse=True
)


result = {

    "system":
    "GENESIS OPPORTUNITY INTELLIGENCE",

    "status":
    "ONLINE",

    "timestamp":
    str(datetime.now()),

    "ranked_opportunities":
    ranked

}


print(json.dumps(result, indent=4))
