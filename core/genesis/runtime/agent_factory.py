import time
import uuid


class GenesisAgentFactory:


    def __init__(
        self,
        generator
    ):

        self.generator = generator

        self.system = (
            "GENESIS AGENT FACTORY v1"
        )


    def build(
        self,
        capability
    ):


        blueprint = self.generator.create(
            capability
        )


        return {

            "id":
                "factory_" +
                uuid.uuid4().hex[:8],

            "blueprint":
                blueprint,

            "status":
                "READY_FOR_REGISTRATION",

            "timestamp":
                time.time()

        }
