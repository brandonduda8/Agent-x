import time
import uuid


class GenesisBusinessMemory:


    def __init__(self):

        self.entries = {}

        self.system = (
            "GENESIS BUSINESS MEMORY v2"
        )


    def store(
        self,
        category,
        data
    ):

        entry_id = (
            "memory_" +
            uuid.uuid4().hex[:8]
        )


        self.entries[entry_id] = {

            "category":
                category,

            "data":
                data,

            "timestamp":
                time.time()

        }


        return self.entries[entry_id]


    def retrieve(
        self,
        category=None
    ):

        if category:

            return {

                k:v for k,v
                in self.entries.items()
                if v["category"] == category

            }


        return self.entries
