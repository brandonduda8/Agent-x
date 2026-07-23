import time

from core.genesis.omega.command_center.state_registry import (
    genesis_state_registry
)


class GenesisStateSyncBridge:

    def __init__(self):
        self.system = "GENESIS STATE SYNC BRIDGE v1"

    def update(self, key, value):

        try:
            genesis_state_registry.set(
                key,
                value
            )

            return {
                "status": "SYNCED",
                "key": key,
                "timestamp": time.time()
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "error": str(e),
                "timestamp": time.time()
            }

    def report(self):

        try:
            return {
                "system": self.system,
                "state": genesis_state_registry.get_all(),
                "timestamp": time.time()
            }

        except Exception as e:

            return {
                "system": self.system,
                "status": "ERROR",
                "error": str(e)
            }


genesis_state_sync_bridge = GenesisStateSyncBridge()
