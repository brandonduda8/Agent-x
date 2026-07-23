import time
import uuid


class GenesisMissionEngine:

    def __init__(
        self,
        task_queue=None,
        event_bus=None
    ):

        self.system = (
            "GENESIS MISSION ENGINE v1"
        )

        self.task_queue = task_queue

        self.event_bus = event_bus



    def create_mission(
        self,
        objective,
        tasks
    ):

        mission_id = (
            "mission_" +
            uuid.uuid4().hex[:8]
        )


        created_tasks = []


        for task in tasks:

            created_tasks.append(

                self.task_queue.add_task(
                    mission_id,
                    task["objective"],
                    task["capability"]
                )

            )


        mission = {

            "id":
                mission_id,

            "objective":
                objective,

            "tasks":
                created_tasks,

            "status":
                "CREATED",

            "timestamp":
                time.time()

        }


        if self.event_bus:

            self.event_bus.publish(
                "MISSION_CREATED",
                mission
            )


        return mission



    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
