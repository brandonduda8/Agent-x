import time
import platform
import json

from core.genesis.tool_registry import tool_registry


class GenesisMasterController:

    def __init__(self):
        self.name = "GENESIS MASTER CONTROLLER v0.1"

        self.identity = {
            "node": "android_primary",
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "python": platform.python_version()
        }

        self.agents = {}


    def register_agent(self, name, agent):

        self.agents[name] = {
            "agent": agent,
            "status": "REGISTERED"
        }

        print(f"🤖 Genesis registered agent: {name}")


    def system_status(self):

        return {
            "genesis": self.name,
            "identity": self.identity,
            "agents": list(self.agents.keys()),
            "tools": tool_registry.available(),
            "timestamp": time.time()
        }


    def discover_capabilities(self):

        tools = tool_registry.available()

        available = []

        for name, data in tools.items():

            if data["installed"]:
                available.append(name)

        return {
            "available_capabilities": available,
            "count": len(available)
        }


    def mission(self, objective):

        return {
            "mission_id": int(time.time()),
            "objective": objective,
            "status": "READY",
            "available_agents": list(self.agents.keys())
        }



genesis_controller = GenesisMasterController()
