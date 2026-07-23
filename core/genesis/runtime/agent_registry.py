import time


class GenesisAgentRegistry:


    def __init__(self):

        self.system = (
            "GENESIS AGENT REGISTRY v1"
        )

        self.agents = {}


    def register(
        self,
        name,
        capabilities
    ):

        self.agents[name] = {

            "capabilities":
                capabilities,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }

        return self.agents[name]


    def list_agents(self):

        return self.agents
