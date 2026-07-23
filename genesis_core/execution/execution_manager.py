import time
import uuid


class GenesisExecutionManager:


    def __init__(self):

        self.tasks = []



    def create_task(
        self,
        mission,
        agent,
        objective
    ):

        task = {

            "id":
            "task_" + uuid.uuid4().hex[:8],

            "mission":
            mission,

            "agent":
            agent,

            "objective":
            objective,

            "status":
            "QUEUED",

            "created":
            time.time()

        }


        self.tasks.append(task)

        return task



    def start_task(self, task_id):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = "RUNNING"

                task["started"] = time.time()


        return self.tasks



    def complete_task(
        self,
        task_id,
        result
    ):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = "COMPLETE"

                task["result"] = result

                task["completed"] = time.time()


        return self.tasks
