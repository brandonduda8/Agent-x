import time

from core.genesis.omega.omega_bootstrap import (
    genesis_omega_bootstrap
)

from core.genesis.omega.command_center.state_registry import (
    genesis_state_registry_bridge
)


class GenesisLiveStateSync:

    def __init__(self):
        self.system = "GENESIS LIVE STATE SYNC BRIDGE v1"

    def sync(self):

        bootstrap = genesis_omega_bootstrap.start()

        state = genesis_state_registry_bridge.report()

        return {
            "system": self.system,
            "status": "SYNC_COMPLETE",
            "bootstrap": bootstrap,
            "state": state,
            "timestamp": time.time()
        }


genesis_live_state_sync = GenesisLiveStateSync()
