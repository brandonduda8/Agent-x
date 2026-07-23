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


from core.genesis.agent_deployment_engine import (
    agent_deployment_engine
)

from core.genesis.worker_registry import (
    worker_registry
)

from core.genesis.workforce_memory import (
    workforce_memory
)

from core.genesis.runtime.agent_harness import (
    genesis_agent_harness
)


class GenesisWorkforceFusionBridge:


    def __init__(self):

        self.system = (
            "GENESIS WORKFORCE FUSION BRIDGE v1"
        )


    def deploy_worker(
        self,
        agent
    ):

        deployment = (
            agent_deployment_engine.deploy(
                agent
            )
        )


        return {

            "deployment":
                deployment,

            "registry":
                worker_registry.report(),

            "memory":
                workforce_memory.report(),

            "timestamp":
                time.time()

        }



    def execute_mission(
        self,
        mission
    ):

        result = (
            genesis_agent_harness.execute(
                mission
            )
        )


        return {

            "system":
                self.system,

            "mission":
                mission,

            "execution":
                result,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "workers":
                worker_registry.report(),

            "memory":
                workforce_memory.report(),

            "harness":
                genesis_agent_harness.report(),

            "timestamp":
                time.time()

        }



genesis_workforce_fusion_bridge = (
    GenesisWorkforceFusionBridge()
)
