import time
import uuid


class GenesisTaskDecomposer:


    def __init__(self):

        self.system = (
            "GENESIS TASK DECOMPOSER v1"
        )


    def decompose(
        self,
        objective
    ):

        tasks = []


        if "client" in objective.lower():

            tasks = [

                {
                    "capability":
                    "research",

                    "objective":
                    "Find potential clients"
                },

                {
                    "capability":
                    "sales",

                    "objective":
                    "Create outreach strategy"
                },

                {
                    "capability":
                    "automation",

                    "objective":
                    "Design delivery solution"
                }

            ]

        else:

            tasks = [

                {
                    "capability":
                    "reasoning",

                    "objective":
                    objective
                }

            ]


        return [

            {
                "id":
                "task_" + uuid.uuid4().hex[:8],

                **task,

                "status":
                "QUEUED",

                "timestamp":
                time.time()

            }

            for task in tasks

        ]
