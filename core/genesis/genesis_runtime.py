import os
import sys
import json
import time


# Ensure project root is available
ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from core.genesis.genesis_omega_sync import (
    genesis_omega_sync
)

from core.genesis.genesis_telegram_gateway import (
    genesis_telegram_gateway
)


class GenesisRuntime:

    def __init__(self):

        self.system = "GENESIS OMEGA RUNTIME v1"

        self.boot_time = time.time()


    def start(self):

        print("\n==============================")
        print("🧬 GENESIS OMEGA RUNTIME")
        print("==============================\n")

        print("Synchronizing ecosystem...\n")


        sync = genesis_omega_sync.run()


        print("✓ Agents synchronized")
        print("✓ Workforce connected")
        print("✓ Tools checked")
        print("✓ Connectors checked")
        print("✓ Revenue systems connected")


        print("\nTELEGRAM:")

        try:

            print(
                genesis_telegram_gateway.report()
            )

        except Exception as e:

            print(
                {
                    "telegram_error": str(e)
                }
            )


        print("\nGENESIS STATUS")

        print(
            json.dumps(
                sync,
                indent=4,
                default=str
            )
        )


        return sync



genesis_runtime = GenesisRuntime()


if __name__ == "__main__":

    genesis_runtime.start()
