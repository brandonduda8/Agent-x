import time

from core.genesis.agent_factory import agent_factory
from core.genesis.agent_deployment_engine import agent_deployment_engine
from core.genesis.worker_registry import worker_registry


class GenesisWorkforceBootstrap:

    def __init__(self):

        self.system = "GENESIS WORKFORCE BOOTSTRAP v1"

        self.boots = []



    def boot(self):

        print(
            "🚀 Genesis Workforce Bootstrap Started"
        )


        agents = []


        print(
            "🤖 Creating Revenue Agent"
        )

        revenue = agent_factory.create_revenue_agent()

        agents.append(
            revenue
        )


        print(
            "🔎 Creating Research Agent"
        )

        research = agent_factory.create_research_agent()

        agents.append(
            research
        )


        print(
            "💼 Creating Career Agent"
        )

        career = agent_factory.create_career_agent()

        agents.append(
            career
        )


        print(
            "💻 Creating Coding Agent"
        )

        coding = agent_factory.create_coding_agent()

        agents.append(
            coding
        )


        deployments = []


        for agent in agents:

            deployment = agent_deployment_engine.deploy(
                agent
            )

            deployments.append(
                deployment
            )


        result = {

            "system":
                self.system,

            "agents_created":
                len(agents),

            "agents":

                [
                    agent["name"]
                    for agent in agents
                ],

            "deployments":

                [
                    deployment["agent"]
                    for deployment in deployments
                ],

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }


        self.boots.append(
            result
        )


        print(
            "✅ Genesis Workforce Online"
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "boots":
                len(self.boots),

            "timestamp":
                time.time()

        }



workforce_bootstrap = GenesisWorkforceBootstrap()
