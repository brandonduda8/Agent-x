import time


from core.genesis.agent_registry import agent_registry
from core.genesis.agent_matching_engine import agent_matching_engine
from core.genesis.genesis_workforce_controller import genesis_workforce_controller
from core.genesis.worker_registry import worker_registry

from core.genesis.tool_registry import tool_registry

from core.genesis.persistent_connector_registry import (
    genesis_persistent_connector_registry
)

from core.genesis.connector_network import (
    genesis_connector_network
)

from core.genesis.revenue_execution_engine import (
    revenue_execution_engine
)

from core.genesis.autonomous_revenue_loop import (
    autonomous_revenue_loop
)


class GenesisOmegaSync:
    """
    GENESIS OMEGA SYNCHRONIZATION LAYER v1

    Purpose:

    Connect existing Genesis systems.

    Authority:

    Registries store.
    Engines decide.
    Workforce executes.
    Runtime coordinates.
    """

    def __init__(self):

        self.system = "GENESIS OMEGA SYNC v1"

        self.history = []

    def sync_agents(self):

        synced = []

        for name, agent in agent_registry.agents.items():

            try:

                agent_matching_engine.register_agent(
                    name,
                    agent.get("skills", [])
                )

                synced.append(name)

            except Exception:
                pass


        return synced


    def sync_workforce(self):

        genesis_workforce_controller.agent_matching_engine = (
            agent_matching_engine
        )

        genesis_workforce_controller.agent_registry = (
            agent_registry
        )

        genesis_workforce_controller.worker_registry = (
            worker_registry
        )

        return {
            "status": "CONNECTED",
            "agents": len(agent_registry.agents)
        }


    def sync_tools(self):

        return tool_registry.report()


    def sync_connectors(self):

        return {
            "persistent":
                genesis_persistent_connector_registry.report(),

            "network":
                genesis_connector_network.report()
        }


    def sync_revenue(self):

        return {
            "execution_engine":
                type(revenue_execution_engine).__name__,

            "autonomous_loop":
                type(autonomous_revenue_loop).__name__
        }


    def run(self):

        result = {

            "system": self.system,

            "agents":
                self.sync_agents(),

            "workforce":
                self.sync_workforce(),

            "tools":
                self.sync_tools(),

            "connectors":
                self.sync_connectors(),

            "revenue":
                self.sync_revenue(),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


        self.history.append(result)


        return result



    def report(self):

        return {

            "system": self.system,

            "syncs":
                len(self.history),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_omega_sync = GenesisOmegaSync()
