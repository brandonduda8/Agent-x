import time


class GenesisAdapterManager:


    def __init__(self):

        self.system = "GENESIS ADAPTER MANAGER v1"

        self.adapters = {}



    def register_adapter(
        self,
        name,
        connector,
        capabilities
    ):

        self.adapters[name] = {

            "connector": connector,

            "capabilities": capabilities,

            "status": "REGISTERED",

            "created": time.time()

        }


        return {

            "adapter": name,

            "status": "REGISTERED"

        }



    def connect_all(self):

        results = []

        for name, adapter in self.adapters.items():

            adapter["status"] = "CONNECTED"

            results.append({

                "adapter": name,

                "status": "CONNECTED",

                "capabilities":
                    adapter["capabilities"]

            })


        return results



    def list_adapters(self):

        return list(
            self.adapters.keys()
        )
