import time

from core.genesis.omega.command_center.genesis_command_bootstrap import (
    genesis_command_bootstrap
)

from core.genesis.omega.command_center.system_health_monitor import (
    genesis_system_health_monitor
)

from core.genesis.omega.command_center.cycle_bridge import (
    genesis_cycle_bridge
)


class GenesisUnifiedCommandCenter:

    def __init__(self):
        self.system = "GENESIS UNIFIED COMMAND CENTER v1"

    def boot(self):

        print("🚀 Starting Genesis Unified Command Center")

        bootstrap = genesis_command_bootstrap.start()

        try:
            cycle = genesis_cycle_bridge.start()
        except Exception as e:
            cycle = {
                "status": "WAITING",
                "error": str(e)
            }

        health = genesis_system_health_monitor.report()

        return {
            "system": self.system,
            "bootstrap": bootstrap,
            "cycle": cycle,
            "health": health,
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_unified_command_center = GenesisUnifiedCommandCenter()
