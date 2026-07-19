import json
import os
import time


class GenesisLaunchMemory:

    def __init__(self):

        self.name = "GENESIS LAUNCH MEMORY v1"

        self.path = "data/genesis_launches.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.memory = self.load()


    def load(self):

        if os.path.exists(self.path):

            try:

                with open(self.path, "r") as f:
                    return json.load(f)

            except Exception:
                pass


        return {
            "launches": []
        }



    def save(self):

        with open(self.path, "w") as f:

            json.dump(
                self.memory,
                f,
                indent=2
            )



    def remember_launch(self, launch):

        record = {

            "timestamp":
                time.time(),

            "idea":
                launch.get("idea"),

            "product":
                launch.get("product"),

            "landing_page":
                launch.get("landing_page")

        }


        self.memory["launches"].append(
            record
        )


        self.save()


        return record



    def latest(self):

        if not self.memory["launches"]:
            return None

        return self.memory["launches"][-1]



    def report(self):

        return {

            "system":
                self.name,

            "launches":
                len(self.memory["launches"]),

            "timestamp":
                time.time()

        }



launch_memory = GenesisLaunchMemory()
