import time

from core.genesis.agent_manager import agent_manager
from core.genesis.runtime.agent_harness import (
    GenesisAgentHarness
)



class GenesisAgentHarnessFusion:


    def __init__(self):

        self.system = (
            "GENESIS AGENT HARNESS FUSION v1"
        )

        self.harness = GenesisAgentHarness()



    def connect_default_agents(self):

        agents = [

            {
                "name":
                "Builder Agent",

                "capabilities":
                [
                    "coding",
                    "deployment",
                    "software"
                ]
            },

            {
                "name":
                "Research Agent",

                "capabilities":
                [
                    "research",
                    "analysis",
                    "market intelligence"
                ]
            },


            {
                "name":
                "Revenue Agent",

                "capabilities":
                [
                    "sales",
                    "marketing",
                    "client acquisition"
                ]
            }

        ]


        connected = []


        for agent in agents:

            result = agent_manager.register(
                agent["name"],
                agent["capabilities"]
            )


            connected.append(
                result
            )


        return {

            "system":
            self.system,

            "agents":
            connected,

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "harness":
            self.harness.report(),

            "timestamp":
            time.time()

        }



genesis_agent_harness_fusion = (
    GenesisAgentHarnessFusion()
)
