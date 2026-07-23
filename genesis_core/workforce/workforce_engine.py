import time
import uuid


class GenesisWorkforceEngine:


    def __init__(self):

        self.agents = []

        self.missions = []



    def register_agent(
        self,
        name,
        specialty,
        capabilities
    ):

        agent = {

            "id":
            "agent_" +
            uuid.uuid4().hex[:8],

            "name":
            name,

            "specialty":
            specialty,

            "capabilities":
            capabilities,

            "performance":
            0,

            "status":
            "AVAILABLE",

            "timestamp":
            time.time()

        }


        self.agents.append(agent)

        return agent



    def find_agent(
        self,
        required_skill
    ):

        matches = [

            agent

            for agent in self.agents

            if required_skill in agent["capabilities"]

        ]


        if not matches:

            return None


        return max(

            matches,

            key=lambda x:

            x["performance"]

        )



    def create_agent_design(
        self,
        missing_capability
    ):

        return {

            "id":
            "design_" +
            uuid.uuid4().hex[:8],

            "name":
            "Genesis Specialist Agent",

            "needed_skill":
            missing_capability,

            "status":
            "DESIGN_READY",

            "timestamp":
            time.time()

        }



    def update_performance(
        self,
        agent_id,
        score
    ):

        for agent in self.agents:

            if agent["id"] == agent_id:

                agent["performance"] = score

                return agent



    def status(self):

        return {

            "system":
            "GENESIS AGENT WORKFORCE EXPANSION ENGINE v1",

            "agents":
            len(self.agents),

            "missions":
            len(self.missions),

            "timestamp":
            time.time()

        }
