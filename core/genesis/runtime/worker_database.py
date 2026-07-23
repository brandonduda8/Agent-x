import time
import uuid


class GenesisWorkerDatabase:


    def __init__(self):

        self.workers = {}


    def register(
        self,
        name,
        worker_type,
        skills
    ):

        worker_id = (
            "worker_" +
            uuid.uuid4().hex[:8]
        )


        worker = {

            "id":
                worker_id,

            "name":
                name,

            "type":
                worker_type,

            "skills":
                skills,

            "status":
                "AVAILABLE",

            "completed_jobs":
                0,

            "timestamp":
                time.time()

        }


        self.workers[worker_id] = worker


        return worker


    def all(self):

        return self.workers
