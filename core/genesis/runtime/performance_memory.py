import time


class GenesisPerformanceMemory:


    def __init__(self):

        self.results = []


    def record(
        self,
        result
    ):

        entry = {

            "result":
                result,

            "timestamp":
                time.time()

        }

        self.results.append(entry)

        return entry


    def get_results(self):

        return self.results
