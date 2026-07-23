import time

from core.genesis.mission_queue import mission_queue


class GenesisMissionCleanup:

    def __init__(self):
        self.system = "GENESIS MISSION CLEANUP v1"


    def recover_stale(self, max_age=600):

        now = time.time()

        recovered = []

        for mission in mission_queue.queue["missions"]:

            if mission.get("status") == "ACTIVE":

                age = now - mission.get(
                    "created",
                    now
                )

                if age > max_age:

                    mission["status"] = "STALLED"

                    mission["recovery"] = (
                        "Recovered stale active mission"
                    )

                    mission["updated"] = now

                    recovered.append(
                        mission["id"]
                    )


        mission_queue.save()

        return {
            "system": self.system,
            "recovered": recovered,
            "count": len(recovered),
            "timestamp": now
        }


mission_cleanup = GenesisMissionCleanup()
