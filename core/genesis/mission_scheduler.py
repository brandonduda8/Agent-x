import time
import uuid


class GenesisMissionScheduler:

    def __init__(self):

        self.name = "GENESIS MISSION SCHEDULER v2"

        self.cycles = 0

        self.missions = []


    def create_mission(
        self,
        objective,
        category="research"
    ):

        self.cycles += 1


        mission = {

            "id":
                "mission_"
                +
                uuid.uuid4().hex[:8],

            "cycle":
                self.cycles,

            "objective":
                objective,

            "category":
                category,

            "status":
                "CREATED",

            "created":
                time.time()

        }


        self.missions.append(
            mission
        )


        return mission



    def execute_cycle(
        self,
        objective,
        category="research"
    ):

        print(
            "🚀 Genesis Mission Cycle Started"
        )


        mission = self.create_mission(
            objective,
            category
        )


        from core.genesis.task_router import task_router
        from core.genesis.execution_engine import execution_engine


        task = task_router.create_task(
            objective,
            category
        )


        execution = execution_engine.execute_task(
            task
        )


        mission["task"] = task

        mission["execution"] = execution

        mission["status"] = "COMPLETE"

        mission["completed"] = time.time()


        print(
            "🧬 Mission Completed"
        )


        return mission



    def report(self):

        return {

            "system":
                self.name,

            "cycles":
                self.cycles,

            "missions":
                len(
                    self.missions
                ),

            "timestamp":
                time.time()

        }



mission_scheduler = GenesisMissionScheduler()
