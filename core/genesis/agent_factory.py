import time
import uuid


class GenesisAgentFactory:

    def __init__(self):

        self.system = "GENESIS AGENT FACTORY v1"
        self.agents = []


    def create_agent(
        self,
        role,
        skills
    ):

        agent = {

            "id":
                "agent_"
                +
                uuid.uuid4().hex[:8],

            "name":
                f"Genesis {role} Agent",

            "role":
                role,

            "skills":
                skills,

            "status":
                "CREATED",

            "created":
                time.time()

        }


        self.agents.append(
            agent
        )


        print(
            "🤖 Agent Created:"
        )

        print(
            agent["name"]
        )


        return agent



    def create_coding_agent(
        self
    ):

        return self.create_agent(
            "Coding",
            [
                "Python",
                "AI Agents",
                "APIs",
                "Automation",
                "Debugging"
            ]
        )



    def create_revenue_agent(
        self
    ):

        return self.create_agent(
            "Revenue",
            [
                "Sales",
                "Outreach",
                "Lead Generation",
                "Proposals",
                "Client Acquisition"
            ]
        )



    def create_career_agent(
        self
    ):

        return self.create_agent(
            "Career",
            [
                "Job Search",
                "Applications",
                "Resume Optimization",
                "Opportunity Research"
            ]
        )



    def create_research_agent(
        self
    ):

        return self.create_agent(
            "Research",
            [
                "Market Research",
                "Analysis",
                "Opportunity Discovery",
                "Data Collection"
            ]
        )



    def report(
        self
    ):

        return {

            "system":
                self.system,

            "agents_created":
                len(
                    self.agents
                ),

            "agents":
                self.agents,

            "timestamp":
                time.time()

        }



agent_factory = GenesisAgentFactory()
