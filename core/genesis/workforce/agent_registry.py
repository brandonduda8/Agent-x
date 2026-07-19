import time
import uuid


class GenesisAgentRegistry:


    def __init__(self):

        self.system = "GENESIS AGENT REGISTRY v1"
        self.agents = []



    def register(
        self,
        name,
        skills
    ):

        print(
            f"🤖 Registering agent: {name}"
        )


        agent = {

            "id":
            "agent_registry_" +
            uuid.uuid4().hex[:8],

            "name": name,

            "skills": skills,

            "performance": 0,

            "level": "JUNIOR",

            "status": "ACTIVE",

            "created": time.time()

        }


        self.agents.append(agent)


        print(
            "✅ Agent registered"
        )


        return agent



    def update_performance(
        self,
        name,
        score
    ):


        for agent in self.agents:

            if agent["name"] == name:

                agent["performance"] = score

                return agent



    def find(
        self,
        skill
    ):


        matches = []


        for agent in self.agents:

            if skill in agent["skills"]:

                matches.append(agent)


        return matches



    def report(self):

        return {

            "system":
            self.system,

            "agents":
            len(self.agents),

            "timestamp":
            time.time()

        }



agent_registry = GenesisAgentRegistry()
