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


from core.genesis.runtime.agent_harness import (
    genesis_agent_harness
)


class GenesisAgentHarnessAdapter:


    def __init__(self):

        self.system = (
            "GENESIS AGENT HARNESS FUSION ADAPTER v1"
        )

        self.harness = genesis_agent_harness



    def connect(self):

        return {

            "system":
                self.system,

            "status":
                "CONNECTED",

            "harness":
                self.harness.report(),

            "timestamp":
                time.time()

        }



    def execute_mission(
        self,
        mission
    ):

        result = self.harness.execute(
            mission
        )


        return {

            "adapter":
                self.system,

            "mission":
                mission,

            "result":
                result,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "runtime":
                self.harness.report(),

            "timestamp":
                time.time()

        }



genesis_agent_harness_adapter = (
    GenesisAgentHarnessAdapter()
)
