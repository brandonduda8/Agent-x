import time

from core.genesis.agent_registry import agent_registry
from core.genesis.agent_matching_engine import agent_matching_engine
from core.genesis.genesis_workforce_controller import genesis_workforce_controller


class GenesisWorkforceSyncEngine:
    """
    GENESIS WORKFORCE SYNC ENGINE v1

    Connects:

    Agent Registry
          |
          v
    Matching Engine
          |
          v
    Workforce Controller
    """


    def __init__(self):

        self.system = "GENESIS WORKFORCE SYNC ENGINE v1"

        self.sync_history = []



    def sync_agents(self):

        count = 0


        for name, agent in agent_registry.agents.items():

            agent_matching_engine.register_agent(
                name,
                agent["skills"]
            )

            count += 1


        genesis_workforce_controller.agent_registry = agent_registry

        genesis_workforce_controller.agent_matching_engine = (
            agent_matching_engine
        )


        result = {

            "system": self.system,

            "agents_synced": count,

            "matching_engine_agents":
            len(agent_matching_engine.agents),

            "status": "CONNECTED",

            "timestamp": time.time()

        }


        self.sync_history.append(result)


        print(
            "🧬 Workforce synchronized"
        )


        return result



    def report(self):

        return {

            "system": self.system,

            "syncs":
            len(self.sync_history),

            "timestamp": time.time()

        }



workforce_sync_engine = GenesisWorkforceSyncEngine()
