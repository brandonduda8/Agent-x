import json
import os
from datetime import datetime


def check(file):
    return os.path.exists(file)


boot = {

    "system": "GENESIS MORNING BOOT",

    "timestamp": str(datetime.now()),

    "operator":
    "Brandon Duda",

    "health": {

        "core":
        "ONLINE",

        "agents":
        "SYNCHRONIZED",

        "adapters":
        "CONNECTED",

        "models":
        "READY",

        "memory":
        "ACTIVE"

    },

    "assets": {

        "opportunity_vault":
        check("opportunities.json"),

        "performance_memory":
        check("genesis_performance_memory.json"),

        "profile":
        check("profile.json")

    },

    "priorities": [

        "Review income opportunities",

        "Review revenue pipeline",

        "Improve Genesis automation"

    ],

    "recommended_action":

    "Complete highest-value income action first"

}


print(json.dumps(boot, indent=4))
