import time


class GenesisAgentSelector:


    def __init__(
        self,
        registry
    ):

        self.registry = registry


    def select(
        self,
        capability
    ):

        matches = []


        for name, agent in self.registry.agents.items():

            if capability in agent["capabilities"]:

                matches.append(name)


        return {

            "capability":
            capability,

            "agents":
            matches,

            "timestamp":
            time.time()

        }
