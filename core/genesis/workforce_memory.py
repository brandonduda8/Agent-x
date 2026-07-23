import json
import os
import time


class WorkforceMemory:

    def __init__(self):

        self.file = "core/genesis/workforce_memory.json"

        self.data = {

            "workers": [],

            "updated":
                time.time()

        }

        self.load()



    def load(self):

        if os.path.exists(self.file):

            with open(
                self.file,
                "r"
            ) as f:

                self.data = json.load(f)



    def save(self):

        self.data["updated"] = time.time()

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4
            )



    def add_worker(
        self,
        worker
    ):

        self.data["workers"].append(
            worker
        )

        self.save()



    def get_workers(self):

        return self.data["workers"]



    def report(self):

        return {

            "system":
                "GENESIS WORKFORCE MEMORY v1",

            "workers":
                len(
                    self.data["workers"]
                ),

            "updated":
                self.data["updated"]

        }



workforce_memory = WorkforceMemory()
