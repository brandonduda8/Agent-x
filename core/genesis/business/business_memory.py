import time


class GenesisBusinessMemory:


    def __init__(self):

        self.system = "GENESIS BUSINESS MEMORY v1"
        self.memory = []


    def store(self, event):

        record = {

            "event":
            event,

            "timestamp":
            time.time()

        }


        self.memory.append(record)


        return record



    def report(self):

        return {

            "system":
            self.system,

            "memories":
            len(self.memory),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



business_memory = GenesisBusinessMemory()
