import time


class GenesisIntegrationRegistry:


    def __init__(self):

        self.integrations = []



    def register(
        self,
        name,
        status,
        details=None
    ):

        self.integrations.append({

            "name": name,

            "status": status,

            "details": details or {},

            "timestamp": time.time()

        })



    def report(self):

        return {

            "system":
            "GENESIS INTEGRATION CONTROL PLANE v1",

            "integrations":
            self.integrations,

            "timestamp":
            time.time()

        }
