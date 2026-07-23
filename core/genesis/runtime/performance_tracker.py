import time


class GenesisPerformanceTracker:


    def __init__(self):

        self.performance = {}


    def record(
        self,
        entity,
        result
    ):

        if entity not in self.performance:

            self.performance[entity] = {

                "total":
                    0,

                "successful":
                    0

            }


        self.performance[entity]["total"] += 1


        if result == "SUCCESS":

            self.performance[entity]["successful"] += 1


        self.performance[entity]["timestamp"] = time.time()


        return self.performance[entity]


    def get_scores(self):

        return self.performance
