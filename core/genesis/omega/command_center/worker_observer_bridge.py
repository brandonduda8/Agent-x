import time
import uuid

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)


class GenesisOmegaWorkerObserverBridge:

    """
    GENESIS OMEGA WORKER OBSERVER BRIDGE v2

    Provides live visibility into Omega workers.
    """


    def __init__(
        self,
        worker_fabric=None,
        heartbeat_system=None
    ):

        self.system = (
            "GENESIS OMEGA WORKER OBSERVER BRIDGE v2"
        )

        self.worker_fabric = (
            worker_fabric
            or genesis_omega_worker_fabric
        )

        self.heartbeat_system = (
            heartbeat_system
        )

        self.snapshots = []


    def sync(self):

        workers = []


        if self.worker_fabric:

            registry = (
                self.worker_fabric.workers
            )


            for capability, worker in registry.items():

                workers.append({

                    "id":
                        "worker_view_"
                        + uuid.uuid4().hex[:8],

                    "capability":
                        capability,

                    "worker":
                        getattr(
                            worker,
                            "name",
                            type(worker).__name__
                        ),

                    "status":
                        "ONLINE",

                    "last_seen":
                        time.time()

                })


        snapshot = {

            "id":
                "observer_"
                + uuid.uuid4().hex[:8],

            "system":
                self.system,

            "workers":
                workers,

            "count":
                len(workers),

            "timestamp":
                time.time()

        }


        self.snapshots.append(
            snapshot
        )


        print(
            "👁️ Worker Observer Sync:",
            len(workers),
            "workers"
        )


        return snapshot



    def report(self):

        latest = (
            self.sync()
        )


        return {

            "system":
                self.system,

            "workers":
                latest["workers"],

            "count":
                latest["count"],

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_worker_observer_bridge = (
    GenesisOmegaWorkerObserverBridge()
)
