import os
import json
import time
import uuid


class GenesisOmegaMissionDatabase:

    """
    GENESIS OMEGA MISSION DATABASE v1

    Persistent mission memory layer.

    Stores:
    - active missions
    - completed missions
    - worker assignments
    - results
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA MISSION DATABASE v1"
        )

        self.file = (
            "data/genesis_omega_missions.json"
        )

        self.missions = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()



    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.missions = json.load(f)

            except Exception:

                self.missions = []



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.missions,
                f,
                indent=2
            )



    def create(
        self,
        objective
    ):

        mission = {

            "id":
                "mission_"
                + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "status":
                "CREATED",

            "workers":
                [],

            "events":
                [],

            "created":
                time.time()

        }


        self.missions.append(
            mission
        )

        self.save()


        print(
            "📋 Mission Created:",
            mission["id"]
        )


        return mission



    def update_status(
        self,
        mission_id,
        status
    ):

        for mission in self.missions:

            if mission["id"] == mission_id:

                mission["status"] = status
                mission["updated"] = time.time()

                self.save()

                return mission


        return None



    def attach_worker(
        self,
        mission_id,
        worker
    ):

        for mission in self.missions:

            if mission["id"] == mission_id:

                mission["workers"].append(
                    worker
                )

                self.save()

                return mission


        return None



    def add_event(
        self,
        mission_id,
        event
    ):

        for mission in self.missions:

            if mission["id"] == mission_id:

                mission["events"].append(
                    event
                )

                self.save()

                return mission


        return None



    def list_all(self):

        return self.missions



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(self.missions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_mission_database = (
    GenesisOmegaMissionDatabase()
)
