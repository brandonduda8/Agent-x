import time
import uuid
import json
import os


class GenesisWorkerBrain:

    """
    GENESIS WORKER BRAIN v1

    Gives Genesis workers memory,
    objectives, and improvement tracking.
    """

    def __init__(self):

        self.system = (
            "GENESIS WORKER BRAIN v1"
        )

        self.file = (
            "data/genesis_worker_memory.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.memory = []

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

                    self.memory = json.load(f)

            except Exception:

                self.memory = []



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.memory,
                f,
                indent=2
            )



    def create_worker_profile(
        self,
        worker_name,
        role,
        goals,
        tools
    ):

        profile = {

            "id":
                "brain_"
                +
                uuid.uuid4().hex[:8],

            "worker":
                worker_name,

            "role":
                role,

            "goals":
                goals,

            "tools":
                tools,

            "completed_tasks": [],

            "improvements": [],

            "decisions": [],

            "created":
                time.time()

        }


        self.memory.append(
            profile
        )


        self.save()


        print(
            f"🧠 Worker brain created: {worker_name}"
        )


        return profile



    def record_task(
        self,
        worker_name,
        task,
        result
    ):

        for worker in self.memory:

            if worker["worker"] == worker_name:

                worker["completed_tasks"].append({

                    "task":
                        task,

                    "result":
                        result,

                    "timestamp":
                        time.time()

                })


                self.save()

                return worker



        return {
            "status":
            "WORKER_NOT_FOUND"
        }



    def add_improvement(
        self,
        worker_name,
        idea
    ):

        for worker in self.memory:

            if worker["worker"] == worker_name:

                worker["improvements"].append({

                    "idea":
                        idea,

                    "timestamp":
                        time.time()

                })


                self.save()

                return worker



        return {
            "status":
            "WORKER_NOT_FOUND"
        }



    def report(self):

        return {

            "system":
                self.system,

            "workers":
                len(
                    self.memory
                ),

            "timestamp":
                time.time()

        }



genesis_worker_brain = GenesisWorkerBrain()
