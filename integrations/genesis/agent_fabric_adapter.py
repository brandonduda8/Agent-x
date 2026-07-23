import time


class AgentFabricAdapter:

    name = "GENESIS AGENT FABRIC ADAPTER v1"

    def __init__(self):
        self.connected_agents = []

    def attach(self, agent_name, role, priority="MEDIUM"):
        agent = {
            "name": agent_name,
            "role": role,
            "priority": priority,
            "status": "ONLINE",
            "timestamp": time.time()
        }

        self.connected_agents.append(agent)

        return agent

    def report(self):
        return {
            "system": self.name,
            "status": "ONLINE",
            "agents": self.connected_agents,
            "count": len(self.connected_agents),
            "timestamp": time.time()
        }


genesis_agent_fabric_adapter = AgentFabricAdapter()
