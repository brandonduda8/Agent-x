import time


class GenesisToolSelector:


    def __init__(
        self,
        connector_fabric
    ):

        self.fabric = connector_fabric

        self.system = (
            "GENESIS TOOL SELECTOR v1"
        )


    def select(
        self,
        capabilities
    ):

        matches = {}


        for capability in capabilities:

            matches[capability] = (
                self.fabric.find_tools(
                    capability
                )
            )


        return {

            "matches": matches,

            "timestamp":
                time.time()

        }
