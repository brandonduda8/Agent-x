import os
import json
import time
import uuid


class GenesisExecutionMemory:


    def __init__(self):

        self.system = (
            "GENESIS EXECUTION MEMORY v1"
        )

        self.file = (
            "data/genesis_execution_memory.json"
        )

        self.records = []

        os.makedirs(
            "data",
            exist_ok=True
        )



    def store(
        self,
        mission,
        results
    ):

        record = {

            "id":
                "memory_" +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "results":
                results,

            "timestamp":
                time.time()

        }


        self.records.append(record)


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.records,
                f,
                indent=2
            )


        return record



    def report(self):

        return {

            "system":
                self.system,

            "memories":
                len(self.records),

            "status":
                "ONLINE"

        }
