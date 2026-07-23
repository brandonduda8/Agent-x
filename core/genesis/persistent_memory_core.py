import time
import uuid
import json
import os


class GenesisPersistentMemoryCore:

    """
    GENESIS PERSISTENT MEMORY CORE v1

    Stores system knowledge.

    Responsibilities:

    - remember opportunities
    - remember worker actions
    - remember executions
    - remember improvements
    - provide historical intelligence
    """

    def __init__(self):

        self.system = (
            "GENESIS PERSISTENT MEMORY CORE v1"
        )

        self.memory_file = (
            "genesis_memory.json"
        )

        self.memory = {

            "events": [],
            "opportunities": [],
            "executions": [],
            "workers": [],
            "improvements": []

        }

        self.load()



    def load(self):

        if os.path.exists(
            self.memory_file
        ):

            try:

                with open(
                    self.memory_file,
                    "r"
                ) as f:

                    self.memory = json.load(
                        f
                    )

            except Exception:

                pass



    def save(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.memory,
                f,
                indent=2
            )



    def remember(
        self,
        category,
        data
    ):

        event = {

            "id":
                "memory_"
                +
                uuid.uuid4().hex[:8],

            "category":
                category,

            "data":
                data,

            "timestamp":
                time.time()

        }


        self.memory["events"].append(
            event
        )


        if category in self.memory:

            self.memory[category].append(
                data
            )


        self.save()


        return event



    def recall(
        self,
        category=None
    ):

        if category:

            return self.memory.get(
                category,
                []
            )


        return self.memory



    def report(self):

        return {

            "system":
                self.system,

            "events":
                len(
                    self.memory["events"]
                ),

            "opportunities":
                len(
                    self.memory["opportunities"]
                ),

            "executions":
                len(
                    self.memory["executions"]
                ),

            "workers":
                len(
                    self.memory["workers"]
                ),

            "improvements":
                len(
                    self.memory["improvements"]
                ),

            "timestamp":
                time.time()

        }



genesis_persistent_memory_core = (
    GenesisPersistentMemoryCore()
)
