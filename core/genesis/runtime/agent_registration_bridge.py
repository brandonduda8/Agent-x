import time


class GenesisAgentRegistrationBridge:


    def __init__(
        self,
        registry
    ):

        self.registry = registry

        self.system = (
            "GENESIS AGENT REGISTRATION BRIDGE v1"
        )


    def register(
        self,
        blueprint
    ):


        return self.registry.register(

            blueprint["name"],

            blueprint["capabilities"]

        )
