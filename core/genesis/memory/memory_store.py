import json
import os
import time
import uuid


class GenesisMemoryStore:

    def __init__(self):

        self.system = "GENESIS MEMORY STORE v1"
        self.file = "data/genesis_memory.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()


    def initialize(self):

        if not os.path.exists(self.file):

            self.save(
                {
                    "memories": []
                }
            )

        else:

            data = self.load()

            if "memories" not in data:

                data["memories"] = []

                self.save(data)



    def load(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def store(
        self,
        agent,
        category,
        content
    ):

        data = self.load()

        if "memories" not in data:

            data["memories"] = []


        memory = {

            "id":
                "memory_" +
                uuid.uuid4().hex[:8],

            "agent":
                agent,

            "category":
                category,

            "content":
                content,

            "created":
                time.time()
        }


        data["memories"].append(
            memory
        )


        self.save(
            data
        )


        print(
            f"🧠 Memory stored: {agent}"
        )


        return memory



    def search(
        self,
        agent
    ):

        data = self.load()

        if "memories" not in data:

            return []


        return [
            memory
            for memory in data["memories"]
            if memory["agent"] == agent
        ]



    def report(self):

        data = self.load()

        return {

            "system":
                self.system,

            "memories":
                len(
                    data.get(
                        "memories",
                        []
                    )
                ),

            "timestamp":
                time.time()
        }



memory_store = GenesisMemoryStore()
