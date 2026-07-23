import time
import uuid


class GenesisWorkQueue:


    def __init__(self):

        self.tasks = []



    def create_task(
        self,
        mission,
        agent
    ):


        task = {


            "id":
            "task_" +
            uuid.uuid4().hex[:8],


            "mission":
            mission["objective"],


            "assigned_agent":
            agent["agent"],


            "status":
            "READY",


            "created":
            time.time()

        }


        self.tasks.append(
            task
        )


        return task



    def list_tasks(self):

        return self.tasks
