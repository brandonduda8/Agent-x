import time
import uuid


class GenesisTaskRouter:

    def __init__(self):

        self.name = (
            "GENESIS TASK ROUTER v1"
        )

        self.tasks = []


        self.agent_map = {

            "research":
                [
                    "Career Command Center",
                    "Opportunity Scanner"
                ],

            "revenue":
                [
                    "Daily Revenue Loop"
                ],

            "learning":
                [
                    "Learning Engine"
                ]

        }


    def create_task(
        self,
        objective,
        category
    ):

        task = {

            "id":
                "task_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "category":
                category,

            "assigned_agents":
                self.agent_map.get(
                    category,
                    []
                ),

            "status":
                "READY",

            "created":
                time.time()

        }


        self.tasks.append(task)


        print(
            "🎯 Task Created:",
            objective
        )

        print(
            "🤖 Assigned:",
            task["assigned_agents"]
        )


        return task



    def report(self):

        return {

            "system":
                self.name,

            "tasks":
                len(self.tasks),

            "timestamp":
                time.time()

        }



task_router = GenesisTaskRouter()
