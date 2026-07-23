import time


class GenesisSalesAnalytics:


    def __init__(self):

        self.system = "GENESIS SALES ANALYTICS v1"

        self.events = []



    def track(
        self,
        event
    ):


        record = {

            "event":
            event,

            "timestamp":
            time.time()

        }


        self.events.append(record)


        return record



    def report(self):

        return {

            "system":
            self.system,

            "events":
            len(self.events),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



sales_analytics = GenesisSalesAnalytics()
