import os
import time

from core.genesis.agent_manager import agent_manager


class GenesisAgentXBridge:


    def __init__(self):

        self.name = "GENESIS AGENT-X BRIDGE v2"

        self.agents = [

            {
                "name":
                    "Builder",

                "capabilities":
                    [
                        "coding",
                        "deployment",
                        "software"
                    ]
            },

            {
                "name":
                    "Researcher",

                "capabilities":
                    [
                        "research",
                        "analysis",
                        "web"
                    ]
            },

            {
                "name":
                    "Revenue",

                "capabilities":
                    [
                        "business",
                        "marketing",
                        "monetization"
                    ]
            }

        ]



    def connect(self):

        connected = []


        for agent in self.agents:

            try:

                result = agent_manager.register(
                    agent["name"],
                    agent["capabilities"]
                )


                connected.append(
                    result["agent"]
                )


                print(
                    f"🧬 [GENESIS] Agent online: {agent['name']}"
                )


            except Exception as e:

                print(
                    f"⚠️ Agent registration failed: {e}"
                )



        return {

            "bridge":
                self.name,

            "connected_agents":
                connected,

            "timestamp":
                time.time()

        }



agent_x_bridge = GenesisAgentXBridge()
