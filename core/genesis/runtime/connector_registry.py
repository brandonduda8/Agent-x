import time


class GenesisConnectorRegistry:


    def __init__(self):

        self.system = (
            "GENESIS CONNECTOR REGISTRY v1"
        )

        self.connectors = {}


    def register(
        self,
        name,
        capabilities
    ):

        self.connectors[name] = {

            "capabilities": capabilities,

            "status": "CONNECTED",

            "timestamp": time.time()

        }


        return self.connectors[name]


    def list_connectors(self):

        return {

            "connectors":
                self.connectors,

            "timestamp":
                time.time()

        }
