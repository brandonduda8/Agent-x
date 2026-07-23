import time


class GenesisResultsAggregator:


    def __init__(self):

        self.system = (
            "GENESIS RESULTS AGGREGATOR v1"
        )


    def collect(
        self,
        results
    ):


        return {

            "results":
                results,

            "insight":
                "Execution data collected",

            "timestamp":
                time.time()

        }
