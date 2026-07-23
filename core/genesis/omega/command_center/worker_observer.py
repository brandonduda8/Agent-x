import time

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.command_center.heartbeat import (
    genesis_heartbeat
)


class GenesisOmegaWorkerObserver:

    """
    GENESIS OMEGA WORKER OBSERVER v1

    Bridges Worker Fabric into Command Center.
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA WORKER OBSERVER v1"
        )


    def sync(self):

        workers = (
            genesis_omega_worker_fabric.workers
        )


        synced = []


        for capability, worker in workers.items():

            name = type(worker).__name__


            genesis_heartbeat.register(
                name,
                capability
            )


            synced.append(
                {
                    "worker": name,
                    "capability": capability
                }
            )


        return {

            "system":
                self.system,

            "synced":
                synced,

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_worker_observer = (
    GenesisOmegaWorkerObserver()
)
