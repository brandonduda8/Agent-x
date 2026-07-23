import time


class GenesisCapabilityRouter:


    def __init__(self, registry):

        self.registry = registry

        self.system = (
            "GENESIS CAPABILITY ROUTER v1"
        )


    def find(
        self,
        capability
    ):

        matches = []

        for name, data in self.registry.connectors.items():

            if capability in data["capabilities"]:

                matches.append(name)


        return {

            "capability":
                capability,

            "available_connectors":
                matches,

            "timestamp":
                time.time()

        }
