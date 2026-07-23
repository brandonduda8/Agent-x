import time
import uuid


class GenesisMissionManager:


    def __init__(self):

        self.missions = []


    def create(
        self,
        objective,
        tasks
    ):

        mission = {

            "id":
                "mission_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "tasks":
                tasks,

            "status":
                "QUEUED",

            "timestamp":
                time.time()

        }


        self.missions.append(mission)

        return mission
