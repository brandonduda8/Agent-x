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

from core.genesis.omega.command_center.genesis_autonomous_cycle_engine import (
    genesis_autonomous_cycle_engine
)


class GenesisUnifiedDashboard:

    """
    GENESIS UNIFIED AUTONOMOUS DASHBOARD v2

    Single system view.
    """

    def __init__(self):

        self.system = (
            "GENESIS UNIFIED AUTONOMOUS DASHBOARD v2"
        )


    def status(self):

        return {

            "system":
                self.system,

            "workers":
                genesis_omega_worker_fabric.report(),

            "missions":
                genesis_mission_database.list_all(),

            "events":
                genesis_event_bus.recent(),

            "autonomous_engine":
                genesis_autonomous_cycle_engine.report(),

            "health":
                {
                    "status":
                        "ONLINE"
                },

            "timestamp":
                time.time()
        }


genesis_unified_dashboard = (
    GenesisUnifiedDashboard()
)
