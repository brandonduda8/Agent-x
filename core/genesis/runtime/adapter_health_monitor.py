import time


class GenesisAdapterHealthMonitor:


    def __init__(
        self,
        manager
    ):

        self.manager = manager

        self.system = (
            "GENESIS ADAPTER HEALTH MONITOR v1"
        )



    def scan(self):

        return {

            "system":
                self.system,

            "adapters":
                self.manager.adapters,

            "status":
                "HEALTH_CHECK_COMPLETE",

            "timestamp":
                time.time()

        }
