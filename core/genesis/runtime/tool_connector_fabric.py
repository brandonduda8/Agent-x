import time


class GenesisToolConnectorFabric:


    def __init__(
        self,
        registry
    ):

        self.registry = registry

        self.system = (
            "GENESIS TOOL CONNECTOR FABRIC v1"
        )



    def find_tools(
        self,
        capability
    ):

        return {

            "capability":
                capability,

            "available_tools":
                self.registry.discover(
                    capability
                ),

            "timestamp":
                time.time()

        }



    def health_report(self):

        return {

            "system":
                self.system,

            "connectors":
                self.registry.health(),

            "status":
                "ONLINE"

        }
