import time


class GenesisIntegrationVerifier:


    def verify(
        self,
        adapters
    ):

        results = []


        for adapter in adapters:

            results.append({

                "name":
                adapter["name"],

                "status":
                adapter["status"],

                "connected":
                adapter["status"]
                in [
                    "READY",
                    "ONLINE"
                ],

                "checked":
                time.time()

            })


        return {

            "system":
            "GENESIS INTEGRATION VERIFIER v1",

            "checks":
            results

        }
