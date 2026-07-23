import time


class GenesisAIModelRegistry:


    def __init__(self):

        self.system = (
            "GENESIS AI MODEL REGISTRY v1"
        )

        self.models = {}


    def register(
        self,
        name,
        capabilities
    ):

        self.models[name] = {

            "capabilities":
                capabilities,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }


        return self.models[name]


    def list_models(self):

        return self.models
