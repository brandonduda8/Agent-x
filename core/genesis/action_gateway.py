import time
import uuid


class GenesisActionGateway:

    def __init__(self):
        self.system = "GENESIS ACTION GATEWAY v1"
        self.actions = []
        self.tools = {}

    def register_tool(
        self,
        name,
        capability,
        handler
    ):
        tool = {
            "id": "tool_" + uuid.uuid4().hex[:8],
            "name": name,
            "capability": capability,
            "handler": handler,
            "status": "AVAILABLE",
            "created": time.time()
        }

        self.tools[name] = tool

        print(
            f"🔧 Tool registered: {name}"
        )

        return tool


    def find_tool(
        self,
        capability
    ):
        for tool in self.tools.values():

            if tool["capability"] == capability:
                return tool

        return None


    def execute_action(
        self,
        agent,
        capability,
        payload=None
    ):

        tool = self.find_tool(
            capability
        )

        action = {
            "id": "action_" + uuid.uuid4().hex[:8],
            "agent": agent,
            "capability": capability,
            "payload": payload,
            "status": "RUNNING",
            "started": time.time()
        }


        if tool:

            result = tool["handler"](
                payload
            )

            action["result"] = result
            action["tool"] = tool["name"]
            action["status"] = "COMPLETED"

        else:

            action["result"] = {
                "message":
                "No external tool connected yet"
            }

            action["status"] = "PENDING_TOOL"


        action["completed"] = time.time()

        self.actions.append(
            action
        )


        print(
            f"⚡ Action executed: {capability}"
        )

        return action


    def report(self):

        return {
            "system": self.system,
            "tools": len(self.tools),
            "actions": len(self.actions),
            "timestamp": time.time()
        }


action_gateway = GenesisActionGateway()
