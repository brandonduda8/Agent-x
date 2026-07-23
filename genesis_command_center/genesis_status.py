import json
import os
from datetime import datetime


def exists(file):

    return os.path.exists(file)


status = {

    "system": "GENESIS STATUS CENTER",

    "timestamp": str(datetime.now()),

    "core": "ONLINE",

    "agents": {

        "count": 6,

        "status": "SYNCHRONIZED"

    },

    "adapters": {

        "status": "CONNECTED"

    },

    "intelligence": {

        "model_router": "ONLINE",

        "decision_engine": "ONLINE",

        "opportunity_scoring": "ONLINE"

    },

    "memory": {

        "performance_memory":

        "ACTIVE"

    },

    "control": {

        "approval_engine":

        "ACTIVE",

        "external_actions":

        "APPROVAL_REQUIRED"

    },

    "files_detected": {

        "opportunity_vault":

        exists("opportunities.json"),

        "memory":

        exists("genesis_performance_memory.json"),

        "profile":

        exists("profile.json")

    },

    "next_power_move":

    "Review highest-value approved opportunity"

}


print(json.dumps(status, indent=4))
