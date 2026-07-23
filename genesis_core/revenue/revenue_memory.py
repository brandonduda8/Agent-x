import time


class GenesisRevenueMemory:


    def __init__(self):

        self.events = []



    def record(
        self,
        event,
        value
    ):

        item = {

            "event":
            event,

            "value":
            value,

            "timestamp":
            time.time()

        }


        self.events.append(item)

        return item



    def history(self):

        return self.events
