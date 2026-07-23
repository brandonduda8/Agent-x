import time


class GenesisCommandCenter:


    def __init__(
        self,
        registry,
        metrics
    ):

        self.registry = registry
        self.metrics = metrics


        self.system = (
            "GENESIS UNIFIED COMMAND CENTER v1"
        )


    def dashboard(self):


        return {

            "system":
                self.system,


            "systems":
                self.registry.all(),


            "metrics":
                self.metrics.snapshot(),


            "status":
                "OPERATIONAL",


            "timestamp":
                time.time()

        }
