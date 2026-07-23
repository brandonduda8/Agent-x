import time

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.command_center.event_bus import (
    genesis_event_bus
)

from core.genesis.omega.command_center.mission_database import (
    genesis_mission_database
)


class GenesisNorthStarKernel:

    """
    GENESIS NORTH STAR KERNEL v2

    Unified autonomous system awareness layer.

    Responsibilities:
    - initialize worker awareness
    - unify missions
    - unify events
    - provide command center state
    - expose autonomous operating status
    """


    def __init__(self):

        self.system = (
            "GENESIS NORTH STAR KERNEL v2"
        )

        self.cycles = 0

        self.created = time.time()


    def sync_workers(self):

        try:

            if not genesis_omega_worker_fabric.workers:

                from core.genesis.omega.genesis_worker_connector import (
                    connect_genesis_workers
                )

                connect_genesis_workers()

            return (
                genesis_omega_worker_fabric.report()
            )

        except Exception as e:

            return {
                "status": "WORKER_SYNC_ERROR",
                "error": str(e),
                "timestamp": time.time()
            }


    def status(self):

        workers = self.sync_workers()

        return {

            "system":
                self.system,

            "workers":
                workers,

            "missions":
                genesis_mission_database.list_all(),

            "events":
                genesis_event_bus.recent(),

            "cycles":
                self.cycles,

            "created":
                self.created,

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


    def heartbeat(self):

        self.cycles += 1

        return self.status()


    def dashboard(self):

        return self.status()


    def report(self):

        return {

            "system":
                self.system,

            "cycles":
                self.cycles,

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


genesis_north_star = GenesisNorthStarKernel()
