import time
import uuid


class GenesisMemoryFabric:


    def __init__(self):

        self.memories = []



    def store(
        self,
        memory_type,
        source,
        data
    ):

        memory = {

            "id":
            "memory_" + uuid.uuid4().hex[:8],

            "type":
            memory_type,

            "source":
            source,

            "data":
            data,

            "timestamp":
            time.time()

        }


        self.memories.append(
            memory
        )


        return memory



    def search(
        self,
        memory_type=None
    ):

        if memory_type is None:

            return self.memories


        return [

            m

            for m in self.memories

            if m["type"] == memory_type

        ]



    def summarize(self):

        categories = {}


        for memory in self.memories:

            category = memory["type"]

            categories[category] = (

                categories.get(
                    category,
                    0
                )

                + 1

            )


        return {

            "system":
            "GENESIS UNIFIED MEMORY FABRIC v1",

            "total_memories":
            len(self.memories),

            "categories":
            categories,

            "timestamp":
            time.time()

        }
