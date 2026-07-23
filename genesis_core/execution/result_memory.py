import time


class GenesisResultMemory:


    def __init__(self):

        self.results = []



    def store(
        self,
        task,
        result
    ):

        memory = {

            "task":
            task,

            "result":
            result,

            "timestamp":
            time.time()

        }


        self.results.append(memory)


        return memory



    def all(self):

        return self.results
