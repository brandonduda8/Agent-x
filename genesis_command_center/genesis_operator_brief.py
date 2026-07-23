import json
from datetime import datetime


with open("vault_profile.json", "r") as file:
    profile = json.load(file)


brief = {

    "system": "GENESIS OPERATOR EXECUTIVE BRIEF",

    "timestamp": str(datetime.now()),

    "operator": {
        "name": profile["operator_profile"]["name"],
        "role": profile["operator_profile"]["system_role"]
    },


    "mission_status": {

        "primary_objectives":
        profile["genesis_preferences"]["primary_objectives"],

        "approval_policy":
        profile["genesis_preferences"]["approval_policy"]

    },


    "daily_power_move": {

        "priority_1":
        "Secure income opportunities",

        "priority_2":
        "Advance revenue pipeline",

        "priority_3":
        "Improve Genesis automation"

    },


    "system_actions": {

        "agents":
        "SYNCHRONIZED",

        "adapters":
        "ONLINE",

        "memory":
        "ACTIVE"

    }

}


print(json.dumps(brief, indent=4))
