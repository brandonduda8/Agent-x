import time
import uuid


class GenesisResultCollector:

    def __init__(self):

        self.name = "GENESIS RESULT COLLECTOR v1"

        self.results = []


    def collect(
        self,
        worker_result
    ):

        record = {

            "id":
                "result_" +
                uuid.uuid4().hex[:8],

            "worker_run":
                worker_result.get("id"),

            "status":
                worker_result.get("status"),

            "results":
                worker_result.get("results"),

            "timestamp":
                time.time()

        }


        self.results.append(
            record
        )


        return record



    def summarize(self):

        return {

            "system":
                self.name,

            "collected_results":
                len(self.results),

            "latest":
                self.results[-1]
                if self.results
                else None,

            "timestamp":
                time.time()

        }



genesis_result_collector = GenesisResultCollector()
