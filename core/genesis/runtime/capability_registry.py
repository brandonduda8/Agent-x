import time
import uuid
import json
import os


class GenesisCapabilityRegistry:

    def __init__(self):

        self.system = (
            "GENESIS CAPABILITY REGISTRY v1"
        )

        self.agents = {}

        self.memory_file = (
            "data/genesis_capabilities.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )


    def register_agent(
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

            "status":
                "REGISTERED",

            "timestamp":
                time.time()

        }


        self.agents[name] = agent

        self._save()

        return agent



    def find_agents(
        self,
        capability
    ):

        results = []

        for agent in self.agents.values():

            if capability in agent["capabilities"]:

                results.append(agent)


        return results



    def _save(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.agents,
                f,
                indent=2
            )



    def report(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.agents),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_capability_registry = (
    GenesisCapabilityRegistry()
)
