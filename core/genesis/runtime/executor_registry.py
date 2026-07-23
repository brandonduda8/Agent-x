import time


class GenesisExecutorRegistry:


    def __init__(self):

        self.executors = {}


    def register(
        self,
        name,
        executor_type,
        capabilities
    ):

        self.executors[name] = {

            "type":
                executor_type,

            "capabilities":
                capabilities,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }


        return self.executors[name]


    def find(
        self,
        capability
    ):

        results = []


        for name, executor in self.executors.items():

            if capability in executor["capabilities"]:

                results.append(name)


        return results
