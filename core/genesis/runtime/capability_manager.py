class GenesisCapabilityManager:


    def __init__(self):

        self.system = (
            "GENESIS CAPABILITY MANAGER v1"
        )


    def find_agent(
        self,
        agents,
        capability
    ):


        for agent in agents:

            if capability in agent["capabilities"]:

                return agent


        return None
