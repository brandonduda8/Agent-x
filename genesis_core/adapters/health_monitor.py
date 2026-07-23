import time


class GenesisHealthMonitor:


    def check(
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

                "health":
                "GOOD"
                if adapter["status"]
                in [
                    "READY",
                    "ONLINE"
                ]
                else
                "UNKNOWN",

                "checked":
                time.time()

            })


        return results
