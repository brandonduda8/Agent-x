import time


from core.genesis.agent_registry import (
    agent_registry
)

from core.genesis.agent_matching_engine import (
    agent_matching_engine
)

from core.genesis.genesis_workforce_controller import (
    genesis_workforce_controller
)

from core.genesis.tool_registry import (
    tool_registry
)

from core.genesis.persistent_connector_registry import (
    genesis_persistent_connector_registry
)

from core.genesis.connector_network import (
    genesis_connector_network
)


class GenesisActivationManager:

    """
    GENESIS OMEGA ACTIVATION MANAGER v1

    Purpose:
    Convert Genesis from connected modules
    into an operational workforce.
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA ACTIVATION MANAGER v1"
        )

        self.activation_history = []


    def activate_agents(self):

        activated = []

        for name, agent in agent_registry.agents.items():

            agent_matching_engine.register_agent(
                name,
                agent.get(
                    "skills",
                    []
                )
            )

            activated.append(name)


        return activated



    def activate_workforce(self):

        genesis_workforce_controller.agent_matching_engine = (
            agent_matching_engine
        )

        genesis_workforce_controller.agent_registry = (
            agent_registry
        )

        return {
            "status": "CONNECTED",
            "agents":
                len(agent_matching_engine.agents)
        }



    def activate_connectors(self):

        connectors = (
            genesis_persistent_connector_registry
            .list_sources()
        )

        return {
            "persistent_sources":
                len(connectors)
        }



    def activate_tools(self):

        return tool_registry.report()



    def activate_network(self):

        return genesis_connector_network.report()



    def activate(self):

        print(
            "\n🧬 GENESIS OMEGA ACTIVATION"
        )

        agents = self.activate_agents()

        workforce = self.activate_workforce()

        connectors = self.activate_connectors()

        tools = self.activate_tools()

        network = self.activate_network()


        report = {

            "system":
                self.system,

            "status":
                "ONLINE",

            "agents":
                agents,

            "workforce":
                workforce,

            "connectors":
                connectors,

            "tools":
                tools,

            "network":
                network,

            "timestamp":
                time.time()
        }


        self.activation_history.append(
            report
        )


        print(
            "✅ Genesis workforce activated"
        )


        return report



    def report(self):

        return {

            "system":
                self.system,

            "activations":
                len(
                    self.activation_history
                ),

            "timestamp":
                time.time()
        }



genesis_activation_manager = (
    GenesisActivationManager()
)
