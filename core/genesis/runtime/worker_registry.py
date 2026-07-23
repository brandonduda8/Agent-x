import uuid
import time


class GenesisWorkerRegistry:


    def __init__(self):

        self.workers = []


    def register(
        self,
        name,
        skills,
        worker_type
    ):

        worker = {

            "id":
                "worker_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "skills":
                skills,

            "type":
                worker_type,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }


        self.workers.append(worker)

        return worker
