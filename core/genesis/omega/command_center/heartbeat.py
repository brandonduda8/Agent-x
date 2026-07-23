import time
import uuid


class GenesisOmegaHeartbeat:

    """
    GENESIS OMEGA HEARTBEAT SYSTEM v1

    Tracks worker health and activity.
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA HEARTBEAT SYSTEM v1"
        )

        self.workers = {}


    def register(
        self,
        worker,
        capability
    ):

        heartbeat = {

            "id":
                "heartbeat_"
                + uuid.uuid4().hex[:8],

            "worker":
                worker,

            "capability":
                capability,

            "status":
                "ONLINE",

            "last_seen":
                time.time(),

            "executions":
                0

        }

        self.workers[worker] = heartbeat

        print(
            "💓 Worker Registered:",
            worker
        )

        return heartbeat



    def pulse(
        self,
        worker,
        activity=None
    ):

        if worker in self.workers:

            self.workers[worker]["last_seen"] = time.time()

            self.workers[worker]["executions"] += 1

            if activity:

                self.workers[worker]["activity"] = activity


            return self.workers[worker]


        return None



    def status(self):

        now = time.time()

        for worker in self.workers.values():

            if now - worker["last_seen"] > 300:

                worker["status"] = "STALE"



        return {

            "system":
                self.system,

            "workers":
                list(self.workers.values()),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_heartbeat = GenesisOmegaHeartbeat()
