import json
from datetime import datetime


class AgentConnector:

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.status = "ONLINE"


    def heartbeat(self):

        return {
            "agent": self.name,
            "status": self.status,
            "heartbeat": str(datetime.now())
        }


    def receive_task(self, task):

        return {
            "agent": self.name,
            "task": task,
            "status": "ACCEPTED",
            "timestamp": str(datetime.now())
        }


    def request_approval(self, action):

        return {
            "agent": self.name,
            "approval_required": True,
            "action": action,
            "status": "WAITING_OPERATOR",
            "timestamp": str(datetime.now())
        }


    def write_memory(self, result):

        return {
            "agent": self.name,
            "memory_update": result,
            "timestamp": str(datetime.now())
        }



agents = [

    AgentConnector(
        "Revenue Agent",
        "Business Development"
    ),

    AgentConnector(
        "Opportunity Discovery Agent",
        "Income Discovery"
    ),

    AgentConnector(
        "Technology Agent",
        "Automation Engineering"
    ),

    AgentConnector(
        "Hermes Agent",
        "Communication Intelligence"
    )

]


output = {

    "system": "GENESIS AGENT CONNECTOR FRAMEWORK",

    "status": "ONLINE",

    "timestamp": str(datetime.now()),

    "interfaces": [

        "heartbeat",

        "receive_task",

        "request_approval",

        "write_memory"

    ],

    "connected_agents": []

}



for agent in agents:

    output["connected_agents"].append({

        "heartbeat": agent.heartbeat(),

        "test_task": agent.receive_task(
            "Synchronize with Genesis Core"
        )

    })



print(json.dumps(output, indent=4))
