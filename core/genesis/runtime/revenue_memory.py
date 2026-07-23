import time


class GenesisRevenueMemory:


    def __init__(self):

        self.history = []

        self.system = (
            "GENESIS REVENUE MEMORY v1"
        )


    def store(
        self,
        result
    ):

        entry = {

            "result":
                result,

            "timestamp":
                time.time()

        }

        self.history.append(
            entry
        )

        return entry


    def recall(self):

        return self.history
