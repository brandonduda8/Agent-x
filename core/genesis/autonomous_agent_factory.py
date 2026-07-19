import time
import uuid


class GenesisAutonomousAgentFactory:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS AGENT FACTORY v1"

        self.created_agents = []



    def create_agent(
        self,
        name,
        role,
        skills
    ):

        agent = {

            "id":
                "agent_" + uuid.uuid4().hex[:8],

            "name":
                name,

            "role":
                role,

            "skills":
                skills,

            "status":
                "CREATED",

            "created":
                time.time()

        }


        self.created_agents.append(
            agent
        )


        print(
            f"🏭 New agent created: {name}"
        )


        return agent



    def spawn_from_capability_gap(
        self,
        capability
    ):

        agent_name = (
            capability
            .replace("_", " ")
            .title()
            + " Agent"
        )


        skills = [
            capability,
            "analysis",
            "execution"
        ]


        return self.create_agent(
            agent_name,
            "Specialized Autonomous Worker",
            skills
        )



    def report(self):

        return {

            "system":
                self.system,

            "agents_created":
                len(self.created_agents),

            "timestamp":
                time.time()

        }



autonomous_agent_factory = GenesisAutonomousAgentFactory()
