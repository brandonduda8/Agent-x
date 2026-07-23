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

from core.genesis.omega.north_star import (
    genesis_north_star
)


class GenesisUnifiedDashboard:

    """
    GENESIS UNIFIED AUTONOMOUS DASHBOARD v1

    Single system visibility layer.

    Tracks:
    - North Star
    - Workers
    - Missions
    - Events
    - System health
    """


    def __init__(self):

        self.system = (
            "GENESIS UNIFIED AUTONOMOUS DASHBOARD v1"
        )

        self.views = 0


    def snapshot(self):

        self.views += 1

        north_star = (
            genesis_north_star.status()
        )

        return {

            "system":
                self.system,

            "north_star":
                north_star,

            "workers":
                genesis_omega_worker_fabric.report(),

            "missions":
                genesis_mission_database.list_all(),

            "events":
                genesis_event_bus.recent(),

            "health":
                {
                    "status": "ONLINE",
                    "views": self.views
                },

            "timestamp":
                time.time()
        }


    def report(self):

        return self.snapshot()


genesis_unified_dashboard = GenesisUnifiedDashboard()
