import os
import sys
import time


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

from genesis_core.fusion.agent_x_adapter import (
    genesis_agent_x_adapter
)

from genesis_core.fusion.agent_harness_adapter import (
    genesis_agent_harness_adapter
)



class GenesisFusionBootstrap:


    def __init__(self):

        self.system = (
            "GENESIS FUSION BOOTSTRAP v1"
        )


    def connect(self):

        connections = []


        systems = [

            (
                "Agent-X Adapter",
                genesis_agent_x_adapter
            ),

            (
                "Agent Harness Adapter",
                genesis_agent_harness_adapter
            )

        ]


        for name, component in systems:

            genesis_kernel.register(
                name,
                component
            )

            connections.append(
                component.connect()
            )


        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "connected":
                connections,

            "kernel":
                genesis_kernel.status(),

            "timestamp":
                time.time()

        }



genesis_fusion_bootstrap = (
    GenesisFusionBootstrap()
)


if __name__ == "__main__":

    import json

    print(
        json.dumps(
            genesis_fusion_bootstrap.connect(),
            indent=4
        )
    )
