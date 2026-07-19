import time
import uuid


class GenesisWorkerRegistry:

    def __init__(self):

        self.system = "GENESIS WORKER REGISTRY v1"

        self.workers = {}


    def register_worker(
        self,
        name,
        role,
        skills
    ):

        worker = {

            "id":
            "worker_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "role":
            role,

            "skills":
            skills,

            "status":
            "ONLINE",

            "created":
            time.time()

        }


        self.workers[name] = worker


        print(
            f"⚙️ Worker registered: {name}"
        )


        return worker



    def get_worker(self, name):

        return self.workers.get(name)



    def list_workers(self):

        return list(
            self.workers.values()
        )



    def report(self):

        return {

            "system":
            self.system,

            "workers":
            len(self.workers),

            "registry":
            self.workers,

            "timestamp":
            time.time()

        }



worker_registry = GenesisWorkerRegistry()
