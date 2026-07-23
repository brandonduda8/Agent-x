import json
from datetime import datetime


def genesis_response(command):

    if command == "/status":

        return {
            "system": "GENESIS",
            "status": "ONLINE",
            "agents": "SYNCHRONIZED",
            "adapters": "CONNECTED",
            "time": str(datetime.now())
        }


    elif command == "/brief":

        return {
            "type": "DAILY POWER BRIEF",
            "priorities": [
                "Secure income",
                "Build revenue pipeline",
                "Improve Genesis automation"
            ],
            "approval_required": True
        }


    elif command == "/nextmove":

        return {
            "next_move":
            "Review highest-value income opportunity",
            "agent":
            "Opportunity Discovery Agent",
            "approval":
            "REQUIRED"
        }


    else:

        return {
            "message":
            "Unknown command",
            "available": [
                "/status",
                "/brief",
                "/nextmove"
            ]
        }


commands = [
    "/status",
    "/brief",
    "/nextmove"
]


output = {

    "system":
    "HERMES GENESIS CONSOLE BRIDGE",

    "status":
    "ONLINE",

    "commands":
    commands,

    "test_responses":
    [
        genesis_response(cmd)
        for cmd in commands
    ]

}


print(json.dumps(output, indent=4))
