import os
import sys
import time


# Ensure claw-os root is available
ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if ROOT not in sys.path:
    sys.path.insert(
        0,
        ROOT
    )


from core.genesis.genesis_kernel import (
    genesis_kernel
)

from core.genesis.agent_manager import (
    agent_manager
)

from genesis_core.fusion.unified_event_fabric import (
    genesis_unified_event_fabric
)


class GenesisFusionRuntime:


    def __init__(self):

        self.system = (
            "GENESIS FUSION RUNTIME v1"
        )


    def boot(self):


        genesis_kernel.register(
            "Unified Event Fabric",
            genesis_unified_event_fabric
        )


        genesis_kernel.register(
            "Agent Manager",
            agent_manager
        )


        event = genesis_unified_event_fabric.publish(
            "SYSTEM_BOOT",
            self.system,
            {
                "kernel":
                genesis_kernel.status()
            }
        )


        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "kernel":
                genesis_kernel.status(),

            "fabric":
                genesis_unified_event_fabric.report(),

            "boot_event":
                event,

            "timestamp":
                time.time()

        }



genesis_fusion_runtime = (
    GenesisFusionRuntime()
)


if __name__ == "__main__":

    import json

    print(
        json.dumps(
            genesis_fusion_runtime.boot(),
            indent=4
        )
    )
