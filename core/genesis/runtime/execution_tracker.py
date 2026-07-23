import time


class GenesisExecutionTracker:


    def __init__(self):

        self.history = []


    def record(
        self,
        execution
    ):

        self.history.append(execution)

        return {

            "recorded":
                True,

            "timestamp":
                time.time()

        }


    def get_history(self):

        return self.history
