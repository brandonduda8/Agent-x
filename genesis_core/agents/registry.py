import time
import uuid


class GenesisAgentRegistry:


    def __init__(self):

        self.agents = []



    def register(
        self,
        name,
        skills
    ):

        agent = {

            "id":
            "agent_" +
            uuid.uuid4().hex[:8],

            "name":
            name,

            "skills":
            skills,

            "status":
            "AVAILABLE",

            "created":
            time.time()

        }


        self.agents.append(
            agent
        )


        return agent



    def list_agents(self):

        return self.agents
