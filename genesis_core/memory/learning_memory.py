import time
import uuid


class GenesisLearningMemory:


    def __init__(self):

        self.memories = []



    def store(
        self,
        event_type,
        data
    ):

        memory = {

            "id":
            "memory_" + uuid.uuid4().hex[:8],

            "type":
            event_type,

            "data":
            data,

            "timestamp":
            time.time()

        }


        self.memories.append(
            memory
        )


        return memory



    def analyze(
        self
    ):

        insights = []


        for memory in self.memories:

            data = memory["data"]


            if "industry" in data:

                insights.append({

                    "pattern":
                    "industry opportunity",

                    "value":
                    data["industry"]

                })


            if "result" in data:

                insights.append({

                    "pattern":
                    "execution outcome",

                    "value":
                    data["result"]

                })


        return insights



    def all(
        self
    ):

        return self.memories
