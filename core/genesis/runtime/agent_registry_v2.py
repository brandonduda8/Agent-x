import time
import uuid


class GenesisAgentRegistryV2:


    def __init__(self):

        self.agents = []

        self.system = (
            "GENESIS AGENT REGISTRY v2"
        )


    def register(
        self,
        name,
        capabilities
    ):

        agent = {

            "id":
                "agent_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "capabilities":
                capabilities,

            "tasks_completed":
                0,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }

        self.agents.append(agent)

        return agent


    def available(self):

        return [

            agent for agent in self.agents

            if agent["status"] == "AVAILABLE"

        ]
