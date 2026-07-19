import asyncio
import time
import traceback


class GenesisKernel:
    """
    GENESIS OS v2 KERNEL

    Core runtime responsible for:
    - keeping Genesis alive
    - registering agents
    - managing plugins
    - dispatching missions
    - system health
    """

    def __init__(self):
        self.system = "GENESIS OS v2 KERNEL"
        self.agents = {}
        self.plugins = {}
        self.events = []
        self.running = False
        self.started = None


    def register_agent(self, name, agent):
        self.agents[name] = agent

        print(f"🧬 Agent registered: {name}")

        return {
            "status": "REGISTERED",
            "agent": name
        }


    def register_plugin(self, name, plugin):
        self.plugins[name] = plugin

        print(f"🔌 Plugin loaded: {name}")

        return {
            "status": "LOADED",
            "plugin": name
        }


    async def emit(self, event, data=None):
        message = {
            "event": event,
            "data": data,
            "timestamp": time.time()
        }

        self.events.append(message)

        print(f"📡 EVENT: {event}")

        return message


    async def start(self):

        if self.running:
            return self.report()

        self.running = True
        self.started = time.time()

        print("""
================================
🧬 GENESIS OS v2 KERNEL ONLINE
================================
""")

        await self.emit(
            "SYSTEM_STARTED",
            {
                "system": self.system
            }
        )

        return self.report()


    async def execute(self, mission):

        print(f"🚀 Kernel executing: {mission}")

        await self.emit(
            "MISSION_STARTED",
            {
                "mission": mission
            }
        )

        results = {}

        for name, agent in self.agents.items():

            try:

                if hasattr(agent, "execute"):

                    results[name] = await agent.execute(mission)

                else:

                    results[name] = {
                        "status": "NO_EXECUTOR"
                    }

            except Exception as e:

                results[name] = {
                    "error": str(e),
                    "trace": traceback.format_exc()
                }


        await self.emit(
            "MISSION_COMPLETED",
            results
        )


        return results


    def report(self):

        return {
            "system": self.system,
            "running": self.running,
            "agents": list(self.agents.keys()),
            "plugins": list(self.plugins.keys()),
            "events": len(self.events),
            "started": self.started,
            "timestamp": time.time()
        }


genesis_kernel = GenesisKernel()
