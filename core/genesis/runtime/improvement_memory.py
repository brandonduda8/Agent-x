import time
import uuid


class GenesisImprovementMemory:


    def __init__(self):

        self.history = []

        self.system = (
            "GENESIS IMPROVEMENT MEMORY v1"
        )


    def store(
        self,
        event
    ):

        record = {

            "id":
                "improvement_" +
                uuid.uuid4().hex[:8],

            "event":
                event,

            "timestamp":
                time.time()

        }

        self.history.append(record)

        return record


    def all(self):

        return self.history
