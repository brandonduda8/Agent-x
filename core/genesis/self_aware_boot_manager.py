import time
import uuid

from core.genesis.identity_core import identity_core
from core.genesis.event_stream import event_stream
from core.genesis.agent_registry import agent_registry
from core.genesis.tool_registry import tool_registry


class GenesisSelfAwareBootManager:

    def __init__(self):

        self.system = "GENESIS SELF-AWARE BOOT MANAGER v1"

        self.boots = []



    def boot(self):

        print(
            "🧬 Genesis self-aware boot starting..."
        )


        identity = identity_core.report()


        restored_agents = []

        restored_tools = []


        data = identity_core.load()


        # Restore agents

        for name, agent in data["agents"].items():

            result = agent_registry.register(

                name,

                agent.get(
                    "role",
                    "Unknown"
                ),

                agent.get(
                    "skills",
                    []
                )

            )

            restored_agents.append(name)



        # Restore tools

        for name, tool in data["tools"].items():

            result = tool_registry.register_tool(

                name,

                tool.get(
                    "category",
                    "general"
                ),

                tool.get(
                    "purpose",
                    ""
                ),

                []

            )

            restored_tools.append(name)



        event = event_stream.emit(

            "GENESIS_BOOT_COMPLETED",

            self.system,

            {

                "agents":
                    restored_agents,

                "tools":
                    restored_tools

            }

        )


        boot = {

            "id":
                "boot_" + uuid.uuid4().hex[:8],

            "identity":
                identity,

            "agents":
                restored_agents,

            "tools":
                restored_tools,

            "timestamp":
                time.time()

        }


        self.boots.append(boot)


        return boot



    def status(self):

        return {

            "system":
                self.system,

            "boots":
                len(self.boots),

            "timestamp":
                time.time()

        }



boot_manager = GenesisSelfAwareBootManager()
