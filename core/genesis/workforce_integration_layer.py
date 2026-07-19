import time

from core.genesis.worker_registry import (
    worker_registry
)

from core.genesis.agent_heartbeat_system import (
    agent_heartbeat_system
)

from core.genesis.agent_matching_engine import (
    agent_matching_engine
)


class GenesisWorkforceIntegrationLayer:

    def __init__(self):

        self.system = "GENESIS WORKFORCE INTEGRATION LAYER v1"

        self.integrations = []


    def integrate_agent(
        self,
        agent
    ):

        name = agent["name"]

        role = agent.get(
            "role",
            "Autonomous Worker"
        )

        skills = agent.get(
            "skills",
            []
        )


        worker = worker_registry.register_worker(
            name,
            role,
            skills
        )


        heartbeat = agent_heartbeat_system.register_agent(
            name,
            role,
            skills
        )


        matcher = agent_matching_engine.register_agent(
            name,
            skills
        )


        record = {

            "agent":
                name,

            "worker":
                worker,

            "heartbeat":
                heartbeat,

            "matcher":
                matcher,

            "status":
                "INTEGRATED",

            "timestamp":
                time.time()

        }


        self.integrations.append(
            record
        )


        print(
            f"🔗 Workforce integrated: {name}"
        )


        return record



    def integrate_workforce(
        self,
        agents
    ):

        results = []


        for agent in agents:

            results.append(
                self.integrate_agent(agent)
            )


        return {

            "system":
                self.system,

            "integrations":
                results,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "integrated_agents":
                len(self.integrations),

            "timestamp":
                time.time()

        }



workforce_integration_layer = GenesisWorkforceIntegrationLayer()
