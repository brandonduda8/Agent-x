import time
import uuid


class GenesisOmegaWorkerDispatcher:
    """
    GENESIS OMEGA WORKER DISPATCHER v1

    Connects capabilities to real Genesis workers.
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA WORKER DISPATCHER v1"
        )

        self.workers = {}

        self.dispatches = []


    def register_worker(
        self,
        capability,
        worker
    ):

        self.workers[capability] = worker


    def dispatch(
        self,
        mission
    ):

        assignments = []


        for capability in mission.get(
            "capabilities",
            []
        ):

            name = capability.get(
                "capability"
            )

            worker = self.workers.get(
                name
            )


            assignments.append(

                {

                    "id":
                        "assignment_"
                        + uuid.uuid4().hex[:8],

                    "capability":
                        name,

                    "worker":
                        str(worker),

                    "status":
                        "READY"

                }

            )


        result = {

            "id":
                "dispatch_"
                + uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "assignments":
                assignments,

            "status":
                "DISPATCHED",

            "created":
                time.time()

        }


        self.dispatches.append(
            result
        )


        return result


    def report(self):

        return {

            "system":
                self.system,

            "workers":
                len(
                    self.workers
                ),

            "dispatches":
                len(
                    self.dispatches
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
