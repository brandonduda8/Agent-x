import time


class GenesisModelRouter:


    def __init__(
        self,
        registry
    ):

        self.registry = registry

        self.system = (
            "GENESIS MODEL ROUTER v1"
        )


    def route(
        self,
        capability
    ):

        available = []


        for name, model in self.registry.models.items():

            if capability in model["capabilities"]:

                available.append(name)


        return {

            "capability":
                capability,

            "models":
                available,

            "timestamp":
                time.time()

        }
