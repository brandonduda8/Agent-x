import time


class GenesisTaskRouter:

    def __init__(self):

        self.system = "GENESIS TASK ROUTER v1"

        self.tasks = []


    def assign(
        self,
        task,
        worker
    ):

        assignment = {

            "task": task,

            "worker": worker,

            "status": "ASSIGNED",

            "timestamp": time.time()

        }

        self.tasks.append(
            assignment
        )

        print(
            f"🧬 Task assigned: {task} -> {worker}"
        )

        return assignment



    def route_mission(
        self,
        objective
    ):

        assignments = []


        if "revenue" in objective.lower() or "client" in objective.lower():

            assignments.append(
                self.assign(
                    "Create high value offer",
                    "Offer Builder"
                )
            )

            assignments.append(
                self.assign(
                    "Find potential customers",
                    "Lead Hunter"
                )
            )

            assignments.append(
                self.assign(
                    "Create marketing content",
                    "Content Agent"
                )
            )

            assignments.append(
                self.assign(
                    "Prepare outreach",
                    "Sales Agent"
                )
            )


        return assignments



    def report(self):

        return {

            "system": self.system,

            "tasks":
            len(self.tasks),

            "assignments":
            self.tasks,

            "timestamp":
            time.time()

        }



task_router = GenesisTaskRouter()
