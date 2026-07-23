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


from core.genesis.agent_x_bridge import (
    agent_x_bridge
)


class GenesisAgentXAdapter:


    def __init__(self):

        self.system = (
            "GENESIS AGENT-X FUSION ADAPTER v1"
        )


    def connect(self):

        connection = (
            agent_x_bridge.connect()
        )


        return {

            "system":
                self.system,

            "status":
                "CONNECTED",

            "agents":
                connection,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_agent_x_adapter = (
    GenesisAgentXAdapter()
)
