import time
import uuid
import os
import json


class GenesisExecutionQueue:

    """
    GENESIS EXECUTION QUEUE v1

    Turns opportunities into actionable missions.

    Handles:

    - task creation
    - worker assignment
    - progress tracking
    - execution history
    """

    def __init__(self):

        self.system = (
            "GENESIS EXECUTION QUEUE v1"
        )

        self.file = (
            "data/genesis_execution_queue.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.tasks = []

        self.load()



    def load(self):

        if os.path.exists(
            self.file
        ):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.tasks = json.load(f)

            except Exception:

                self.tasks = []



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.tasks,
                f,
                indent=2
            )



    def create_execution(
        self,
        opportunity,
        worker="Opportunity Hunter"
    ):

        category = (
            opportunity.get(
                "category",
                ""
            )
            .upper()
        )


        if category in [
            "JOB",
            "FREELANCE"
        ]:

            steps = [

                "Analyze opportunity",
                "Create customized application",
                "Generate outreach",
                "Submit application",
                "Track response"

            ]

        elif category in [
            "CLIENT",
            "BUSINESS"
        ]:

            steps = [

                "Validate business",
                "Research pain points",
                "Prepare automation offer",
                "Find sales closer",
                "Track deal"

            ]

        else:

            steps = [

                "Research",
                "Analyze",
                "Recommend action"

            ]



        execution = {

            "id":
                "execution_"
                +
                uuid.uuid4().hex[:8],


            "opportunity":
                opportunity,


            "worker":
                worker,


            "steps":
                steps,


            "current_step":
                0,


            "status":
                "READY",


            "created":
                time.time()

        }


        self.tasks.append(
            execution
        )


        self.save()


        print(
            "🚀 Execution created:"
        )

        print(
            opportunity.get(
                "title"
            )
        )


        return execution



    def update_progress(
        self,
        execution_id
    ):

        for task in self.tasks:

            if task["id"] == execution_id:

                task["current_step"] += 1


                if (
                    task["current_step"]
                    >=
                    len(task["steps"])
                ):

                    task["status"] = (
                        "COMPLETED"
                    )

                else:

                    task["status"] = (
                        "IN_PROGRESS"
                    )


                self.save()

                return task


        return {
            "status":
            "NOT_FOUND"
        }



    def report(self):

        return {

            "system":
                self.system,


            "tasks":
                len(
                    self.tasks
                ),


            "timestamp":
                time.time()

        }



genesis_execution_queue = GenesisExecutionQueue()
