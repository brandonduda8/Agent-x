import os
import sys
import time

# Ensure claw-os root is available for Genesis imports
ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from core.genesis.omega.command_center.genesis_unified_command_center import (
    genesis_unified_command_center
)


class GenesisSystemLauncher:

    def __init__(self):
        self.system = "GENESIS MASTER LAUNCHER v1"

    def start(self):

        print("🌌 Starting Genesis Master System...")
        print("=================================")

        result = genesis_unified_command_center.boot()

        return {
            "system": self.system,
            "genesis": result,
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_launcher = GenesisSystemLauncher()


if __name__ == "__main__":

    result = genesis_launcher.start()

    print("")
    print("=================================")
    print("✅ GENESIS SYSTEM ONLINE")
    print("=================================")
    print(result)
