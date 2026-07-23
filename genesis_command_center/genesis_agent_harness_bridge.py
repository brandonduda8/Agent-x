import json
from datetime import datetime


task = {

    "mission_id": 7,

    "agent":
    "Revenue Agent",

    "action":
    "Send client outreach",

    "status":
    "APPROVED"

}


def send_to_harness(task):

    if task["status"] != "APPROVED":

        return {

            "status":
            "BLOCKED",

            "reason":
            "Approval missing"

        }


    return {

        "agent":
        task["agent"],

        "task_received":
        task["action"],

        "harness_status":
        "ACCEPTED",

        "execution_status":
        "RUNNING",

        "timestamp":
        str(datetime.now())

    }



result = {

    "system":
    "GENESIS AGENT HARNESS BRIDGE",

    "status":
    "ONLINE",

    "interface":
    [
        "receive_task",
        "execute",
        "report_result"
    ],

    "task":
    send_to_harness(task)

}


print(
    json.dumps(
        result,
        indent=4
    )
)
