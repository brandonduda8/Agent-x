import time
import uuid


class GenesisTaskQueue:


    def __init__(self):

        self.tasks = {}

        self.system = (
            "GENESIS TASK QUEUE v1"
        )


    def add_task(
        self,
        task,
        executor
    ):

        task_id = (
            "execution_task_" +
            uuid.uuid4().hex[:8]
        )


        self.tasks[task_id] = {

            "id":
                task_id,

            "task":
                task,

            "executor":
                executor,

            "status":
                "QUEUED",

            "timestamp":
                time.time()

        }


        return self.tasks[task_id]


    def list_tasks(self):

        return self.tasks
