import time


class GenesisTaskDispatcher:


    def __init__(self):

        self.system = (
            "GENESIS TASK DISPATCHER v1"
        )



    def dispatch(self, tasks):

        queue = []

        for task in tasks:

            queue.append({

                "task_id":
                    task["id"],

                "agent":
                    task["agent"],

                "capability":
                    task["capability"],

                "mission":
                    task["mission"],

                "status":
                    "DISPATCHED"

            })


        return {

            "tasks":
                queue,

            "timestamp":
                time.time()

        }
