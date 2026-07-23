import time


class GenesisResultCollector:


    def __init__(self):

        self.results = []

        self.system = (
            "GENESIS RESULT COLLECTOR v1"
        )



    def collect(self, result):

        self.results.append(
            result
        )


        return {

            "stored":
                True,

            "total_results":
                len(self.results),

            "timestamp":
                time.time()

        }
