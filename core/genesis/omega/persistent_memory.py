import os
import json
import time
import uuid


class GenesisOmegaPersistentMemory:

    """
    GENESIS OMEGA PERSISTENT MEMORY CORE v2

    Safe long-term memory storage.
    Prevents circular references.
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA PERSISTENT MEMORY CORE v2"
        )

        self.file = (
            "data/omega_memory.json"
        )

        self.memory = []

        self.load()



    def load(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    data = json.load(f)

                    self.memory = data.get(
                        "memory",
                        []
                    )

            except Exception:

                self.memory = []



    def sanitize(self, obj):

        """
        Converts objects into JSON-safe data.
        Removes recursive references.
        """

        if isinstance(obj, dict):

            clean = {}

            for key, value in obj.items():

                if key in [
                    "learning",
                    "controller",
                    "router"
                ]:

                    continue

                clean[key] = self.sanitize(
                    value
                )

            return clean


        if isinstance(obj, list):

            return [
                self.sanitize(x)
                for x in obj
            ]


        try:

            json.dumps(obj)

            return obj

        except Exception:

            return str(obj)



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        safe_memory = self.sanitize(
            self.memory
        )


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(

                {
                    "system":
                        self.system,

                    "memory":
                        safe_memory,

                    "updated":
                        time.time()
                },

                f,

                indent=2
            )



    def remember(
        self,
        event
    ):

        safe_event = self.sanitize(
            event
        )


        record = {

            "id":
                "omega_memory_"
                +
                uuid.uuid4().hex[:8],

            "event":
                safe_event,

            "created":
                time.time()

        }


        self.memory.append(
            record
        )


        self.save()


        print(
            "💾 Omega Memory Stored:",
            record["id"]
        )


        return record



    def recall(
        self,
        keyword=None
    ):

        if not keyword:

            return self.memory


        results = []


        for item in self.memory:

            if keyword.lower() in str(item).lower():

                results.append(
                    item
                )


        return results



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



genesis_omega_persistent_memory = (
    GenesisOmegaPersistentMemory()
)
