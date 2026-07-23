import time


class GenesisTaskAllocator:


    def assign(
        self,
        mission,
        agents
    ):

        assignments = []


        for task in mission["tasks"]:

            assignments.append({

                "task":
                    task,

                "assigned_to":
                    agents,

                "status":
                    "QUEUED"

            })


        return {

            "mission":
                mission["id"],

            "assignments":
                assignments,

            "timestamp":
                time.time()

        }
