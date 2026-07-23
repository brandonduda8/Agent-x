import json
from datetime import datetime


notifications = [

    {
        "type":
        "APPROVAL_REQUIRED",

        "priority":
        "HIGH",

        "from":
        "Revenue Agent",

        "action":
        "Send approved client outreach",

        "impact":
        "Potential revenue opportunity",

        "response":
        "APPROVE 1 or DENY 1"

    },


    {
        "type":
        "DAILY_BRIEF",

        "priority":
        "NORMAL",

        "from":
        "Hermes Agent",

        "message":
        "Genesis daily intelligence briefing ready"

    }

]


output = {

    "system":
    "GENESIS NOTIFICATION CENTER",

    "status":
    "ONLINE",

    "timestamp":
    str(datetime.now()),

    "queue_size":
    len(notifications),

    "notifications":
    notifications

}


print(json.dumps(output, indent=4))
