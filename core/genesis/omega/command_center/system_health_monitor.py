import time

from core.genesis.omega.command_center.state_registry import (
    genesis_state_registry_bridge
)


class GenesisSystemHealthMonitor:

    def __init__(self):
        self.system = "GENESIS SYSTEM HEALTH MONITOR v2"

    def report(self):

        state = genesis_state_registry_bridge.report()

        return {
            "system": self.system,
            "status": "ONLINE",
            "live_state": state,
            "timestamp": time.time()
        }


genesis_system_health_monitor = GenesisSystemHealthMonitor()
