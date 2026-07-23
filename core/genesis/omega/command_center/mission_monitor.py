import time
import uuid


class GenesisMissionMonitor:

    """
    GENESIS OMEGA MISSION MONITOR v1

    Live observation layer for autonomous missions.
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA MISSION MONITOR v1"
        )

        self.active = {}
        self.completed = []


    def start(
        self,
        objective
    ):

        mission_id = (
            "mission_"
            + uuid.uuid4().hex[:8]
        )

        mission = {
            "id": mission_id,
            "objective": objective,
            "status": "RUNNING",
            "workers": [],
            "started": time.time()
        }

        self.active[mission_id] = mission

        print(
            "🚀 Mission Started:",
            mission_id
        )

        return mission


    def attach_worker(
        self,
        mission_id,
        worker
    ):

        if mission_id in self.active:

            self.active[mission_id]["workers"].append(
                worker
            )

        return self.active.get(
            mission_id
        )


    def complete(
        self,
        mission_id,
        result
    ):

        if mission_id in self.active:

            mission = self.active.pop(
                mission_id
            )

            mission["status"] = "COMPLETE"
            mission["result"] = result
            mission["completed"] = time.time()

            self.completed.append(
                mission
            )

            print(
                "✅ Mission Complete:",
                mission_id
            )

            return mission


    def snapshot(self):

        return {

            "system":
                self.system,

            "active":
                list(
                    self.active.values()
                ),

            "completed":
                self.completed[-20:],

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


genesis_mission_monitor = GenesisMissionMonitor()
