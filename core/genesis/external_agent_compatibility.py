import time
import os


class ExternalAgentCompatibility:

    def __init__(self):

        self.agents = [
            {
                "name": "OpenHands",
                "type": "software_engineering_agent",
                "adapter": "core/genesis/openhands_adapter.py",
                "status": self.check(
                    "core/genesis/openhands_adapter.py"
                )
            },
            {
                "name": "Manus",
                "type": "autonomous_execution_agent",
                "adapter": "MANUS_COMPATIBILITY_LAYER",
                "status": "PENDING_CONNECTION"
            },
            {
                "name": "Open Interpreter",
                "type": "computer_execution_agent",
                "adapter": "core/genesis/open_interpreter_adapter.py",
                "status": self.check(
                    "core/genesis/open_interpreter_adapter.py"
                )
            }
        ]


    def check(self, path):

        if os.path.exists(path):
            return "ADAPTER_FOUND"

        return "MISSING"


    def status(self):

        return {
            "system": "GENESIS EXTERNAL AGENT FABRIC v1",
            "status": "ONLINE",
            "agents": self.agents,
            "timestamp": time.time()
        }


external_agent_compatibility = ExternalAgentCompatibility()
