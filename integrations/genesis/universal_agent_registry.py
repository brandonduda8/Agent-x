import time


class UniversalAgentRegistry:

    def __init__(self):
        self.agents = []

    def register(self, agent):
        self.agents.append(agent)
        return {
            "system": "GENESIS UNIVERSAL AGENT REGISTRY v1",
            "status": "REGISTERED",
            "agent": getattr(agent, "name", "UNKNOWN"),
            "timestamp": time.time()
        }

    def report(self):
        return {
            "system": "GENESIS UNIVERSAL AGENT REGISTRY v1",
            "agents": [
                getattr(agent, "name", "UNKNOWN")
                for agent in self.agents
            ],
            "count": len(self.agents),
            "timestamp": time.time()
        }


genesis_agent_registry = UniversalAgentRegistry()
