import time

from core.genesis.omega.command_center.genesis_autonomous_cycle_engine import (
    genesis_autonomous_cycle_engine
)


class GenesisCycleBridge:
    """
    GENESIS AUTONOMOUS CYCLE BRIDGE v1

    Connects Unified Dashboard
    to Autonomous Cycle Engine.
    """

    def __init__(self):
        self.system = "GENESIS AUTONOMOUS CYCLE BRIDGE v1"

    def start(self):
        try:
            result = genesis_autonomous_cycle_engine.run_cycle()

            return {
                "system": self.system,
                "status": "ONLINE",
                "cycle": result,
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "system": self.system,
                "status": "ERROR",
                "error": str(e),
                "timestamp": time.time()
            }


genesis_cycle_bridge = GenesisCycleBridge()
