import time


class GenesisMetricsCollector:


    def __init__(self):

        self.metrics = {


            "opportunities":
                0,


            "leads":
                0,


            "revenue":
                0,


            "workers":
                0,


            "missions":
                0


        }


    def update(
        self,
        category,
        value
    ):

        self.metrics[category] = value

        return self.metrics


    def snapshot(self):

        return {

            "metrics":
                self.metrics,

            "timestamp":
                time.time()

        }
