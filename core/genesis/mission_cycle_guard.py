import time
import json
import os


class GenesisMissionCycleGuard:
    """
    GENESIS MISSION CYCLE GUARD v1

    Prevents duplicate autonomous mission loops.
    """

    def __init__(self):
        self.file = "data/genesis_cycle_guard.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.state = self.load()


    def load(self):

        if os.path.exists(self.file):

            try:
                with open(self.file,"r") as f:
                    return json.load(f)

            except:
                pass

        return {
            "last_mission": None,
            "last_time": 0,
            "runs": 0
        }


    def save(self):

        with open(self.file,"w") as f:
            json.dump(
                self.state,
                f,
                indent=2
            )


    def allow(self, mission_name, cooldown=300):

        now = time.time()

        if (
            self.state["last_mission"] == mission_name
            and
            now - self.state["last_time"] < cooldown
        ):
            return False


        self.state["last_mission"] = mission_name
        self.state["last_time"] = now
        self.state["runs"] += 1

        self.save()

        return True


    def report(self):

        return {
            "system":
                "GENESIS MISSION CYCLE GUARD v1",

            "state":
                self.state,

            "timestamp":
                time.time()
        }



mission_cycle_guard = GenesisMissionCycleGuard()
