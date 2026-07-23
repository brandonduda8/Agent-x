import time


class GenesisModelMemory:


    def __init__(self):

        self.history = []



    def record(
        self,
        agent,
        model,
        result
    ):

        self.history.append({

            "agent":
            agent,

            "model":
            model,

            "result":
            result,

            "timestamp":
            time.time()

        })


    def get_history(self):

        return self.history
