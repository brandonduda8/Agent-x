import json
from datetime import datetime


pending = {

    "id": 7,

    "agent":
    "Revenue Agent",

    "action":
    "Send client outreach",

    "impact":
    "Potential revenue opportunity",

    "status":
    "WAITING"

}


def process_command(command):

    if command == "/approve 7":

        pending["status"] = "APPROVED"

    elif command == "/deny 7":

        pending["status"] = "DENIED"

    return pending



output = {

    "system":
    "HERMES APPROVAL ROUTER",

    "timestamp":
    str(datetime.now()),

    "request":
    pending,

    "test":

    [
        process_command("/approve 7")
    ]

}


print(
    json.dumps(
        output,
        indent=4
    )
)
