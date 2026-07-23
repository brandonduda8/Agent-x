import time

from core.genesis.omega.command_center.genesis_live_state_sync import (
    genesis_live_state_sync
)


class GenesisNorthStarHeartbeat:

    def __init__(self):
        self.system = "GENESIS NORTH STAR HEARTBEAT v1"
        self.beats = 0

    def pulse(self):

        self.beats += 1

        state = genesis_live_state_sync.sync()

        return {
            "system": self.system,
            "status": "ONLINE",
            "heartbeat": self.beats,
            "workers": state["state"]["workers"],
            "missions": state["state"]["missions"],
            "timestamp": time.time()
        }


genesis_north_star_heartbeat = GenesisNorthStarHeartbeat()
