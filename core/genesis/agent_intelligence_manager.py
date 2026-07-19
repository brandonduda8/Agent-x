import time
import uuid


class GenesisAgentIntelligenceManager:

    def __init__(self):

        self.system = "GENESIS AGENT INTELLIGENCE MANAGER v1"

        self.agents = []


    def create_agent(
        self,
        name,
        role,
        tools,
        permissions,
        llm
    ):

        agent = {

            "id":
            "agent_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "role":
            role,

            "tools":
            tools,

            "permissions":
            permissions,

            "llm":
            llm,

            "status":
            "ONLINE",

            "created":
            time.time()

        }


        self.agents.append(agent)


        print(
            f"🧬 Intelligent Agent Created: {name}"
        )


        return agent



    def connect_llm(
        self,
        agent,
        llm
    ):

        for item in self.agents:

            if item["name"] == agent:

                item["llm"] = llm

                return {

                    "agent": agent,

                    "llm": llm,

                    "status": "CONNECTED",

                    "timestamp": time.time()

                }


        return None



    def report(self):

        return {

            "system":
            self.system,

            "agents":
            len(self.agents),

            "registry":
            self.agents,

            "timestamp":
            time.time()

        }



agent_intelligence_manager = GenesisAgentIntelligenceManager()
