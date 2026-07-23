import os
import json
import time
import uuid


class GenesisMemoryVault:
    """
    GENESIS MEMORY VAULT v1

    Long-term knowledge storage for Genesis agents.

    Stores:
    - missions
    - agent outputs
    - strategies
    - experiments
    - performance data
    """

    def __init__(self):

        self.name = "GENESIS MEMORY VAULT v1"

        self.storage_path = (
            "core/genesis/data/genesis_memory.json"
        )

        self._initialize_storage()


    def _initialize_storage(self):

        directory = os.path.dirname(
            self.storage_path
        )

        os.makedirs(
            directory,
            exist_ok=True
        )

        if not os.path.exists(
            self.storage_path
        ):

            with open(
                self.storage_path,
                "w"
            ) as f:

                json.dump(
                    {
                        "memories": [],
                        "created": time.time()
                    },
                    f,
                    indent=2
                )


    def _load(self):

        with open(
            self.storage_path,
            "r"
        ) as f:

            return json.load(f)


    def _save(self, data):

        with open(
            self.storage_path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )


    def remember(
        self,
        category,
        agent,
        objective,
        result,
        score=None
    ):

        data = self._load()

        memory = {

            "id":
                "memory_" +
                uuid.uuid4().hex[:8],

            "category": category,

            "agent": agent,

            "objective": objective,

            "result": result,

            "score": score,

            "timestamp":
                time.time()

        }


        data["memories"].append(
            memory
        )


        self._save(
            data
        )


        return memory



    def recall(
        self,
        keyword=None,
        category=None
    ):

        data = self._load()

        memories = data.get(
            "memories",
            []
        )


        results = []


        for memory in memories:

            match = True


            if keyword:

                text = json.dumps(
                    memory
                ).lower()

                if keyword.lower() not in text:

                    match = False


            if category:

                if memory.get(
                    "category"
                ) != category:

                    match = False


            if match:

                results.append(
                    memory
                )


        return results



    def status(self):

        data = self._load()

        return {

            "system":
                self.name,

            "memories":
                len(
                    data.get(
                        "memories",
                        []
                    )
                ),

            "storage":
                self.storage_path,

            "timestamp":
                time.time()

        }



genesis_memory_vault = GenesisMemoryVault()
