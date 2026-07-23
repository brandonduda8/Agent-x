import time


class GenesisDecisionMemory:


    def __init__(self):

        self.history = []


    def record(
        self,
        decision
    ):

        entry = {

            "decision":
                decision,

            "timestamp":
                time.time()

        }

        self.history.append(entry)

        return entry


    def get_history(self):

        return self.history
