import time

from core.genesis.omega.command_center.genesis_north_star_heartbeat import (
    genesis_north_star_heartbeat
)


class GenesisNorthStarControllerLoop:

    def __init__(self):
        self.system = "GENESIS NORTH STAR CONTROLLER LOOP v1"
        self.cycles = 0
        self.status = "READY"

    def run_cycle(self):

        self.cycles += 1

        heartbeat = genesis_north_star_heartbeat.pulse()

        self.status = "ONLINE"

        return {
            "system": self.system,
            "status": self.status,
            "cycle": self.cycles,
            "heartbeat": heartbeat,
            "timestamp": time.time()
        }

    def report(self):

        return {
            "system": self.system,
            "status": self.status,
            "cycles": self.cycles,
            "timestamp": time.time()
        }


genesis_north_star_controller_loop = GenesisNorthStarControllerLoop()
