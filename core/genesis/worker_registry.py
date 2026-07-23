import time


class GenesisWorkerRegistry:

    def __init__(self):
        self.system = "GENESIS WORKER REGISTRY v2.2"
        self.workers = []


    def register(self, worker):

        if isinstance(worker, dict):

            record = {
                "id": worker.get("id"),
                "name": worker.get("name", "Unknown Worker"),
                "capability": worker.get("role", "unknown"),
                "skills": worker.get("skills", []),
                "missions": 0,
                "performance": 100,
                "status": "ONLINE",
                "worker_object": worker,
                "created": time.time()
            }

        else:

            record = {
                "id": getattr(worker, "id", None),
                "name": getattr(worker, "name", "Unknown Worker"),
                "capability": getattr(worker, "capability", "unknown"),
                "skills": getattr(worker, "skills", []),
                "missions": 0,
                "performance": 100,
                "status": "ONLINE",
                "worker_object": worker,
                "created": time.time()
            }


        self.workers.append(record)

        print(
            "🧬 Worker Registered:",
            record["name"]
        )

        return record


    def get_online_workers(self):

        return [
            worker
            for worker in self.workers
            if worker["status"] == "ONLINE"
        ]


    def report(self):

        return {
            "system": self.system,
            "workers": [
                {
                    "id": worker["id"],
                    "name": worker["name"],
                    "capability": worker["capability"],
                    "skills": worker["skills"],
                    "missions": worker["missions"],
                    "performance": worker["performance"],
                    "status": worker["status"]
                }
                for worker in self.workers
            ],
            "count": len(self.workers),
            "timestamp": time.time()
        }



worker_registry = GenesisWorkerRegistry()
