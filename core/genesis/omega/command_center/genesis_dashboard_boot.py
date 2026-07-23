import time

from core.genesis.omega.genesis_worker_connector import (
    connect_genesis_workers
)

from core.genesis.omega.command_center.genesis_unified_dashboard import (
    genesis_unified_dashboard
)

from core.genesis.omega.command_center.genesis_autonomous_cycle_engine import (
    genesis_autonomous_cycle_engine
)


class GenesisDashboardBoot:

    def __init__(self):
        self.system = "GENESIS DASHBOARD BOOT v1"


    def start(self):

        print("🚀 Starting Genesis Unified Dashboard...")


        workers = connect_genesis_workers()


        try:
            cycle = (
                genesis_autonomous_cycle_engine.run()
            )

        except Exception as e:
            cycle = {
                "status": "WAITING",
                "error": str(e)
            }


        dashboard = (
            genesis_unified_dashboard.status()
        )


        return {

            "system":
                self.system,

            "workers":
                workers,

            "cycle":
                cycle,

            "dashboard":
                dashboard,

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


genesis_dashboard_boot = GenesisDashboardBoot()
