import time

from core.genesis.omega.command_center.genesis_agent_harness import (
    genesis_agent_harness
)


class GenesisHarnessDashboardBridge:

    def __init__(self):
        self.system = "GENESIS HARNESS DASHBOARD BRIDGE v1"

    def report(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "harness": genesis_agent_harness.report(),
            "timestamp": time.time()
        }


genesis_harness_dashboard_bridge = GenesisHarnessDashboardBridge()
