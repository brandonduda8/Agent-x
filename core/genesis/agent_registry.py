import time
import uuid


class GenesisAgentRegistry:

    def __init__(self):

        self.system = "GENESIS AGENT REGISTRY v1"

        self.agents = {}



    def register(
        self,
        name,
        role,
        skills,
        interface="LOCAL"
    ):

        agent_id = "agent_" + uuid.uuid4().hex[:8]

        agent = {

            "id": agent_id,

            "name": name,

            "role": role,

            "skills": skills,

            "interface": interface,

            "status": "ONLINE",

            "created": time.time()

        }


        self.agents[name] = agent


        print(f"🧬 Agent registered: {name}")


        return agent



    def get(self,name):

        return self.agents.get(name)



    def list_agents(self):

        return list(self.agents.values())



    def report(self):

        return {

            "system": self.system,

            "agents": len(self.agents),

            "registry": self.agents,

            "timestamp": time.time()

        }



agent_registry = GenesisAgentRegistry()
