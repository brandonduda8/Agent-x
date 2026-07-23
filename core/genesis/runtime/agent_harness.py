import time
import uuid


class GenesisAgentHarness:

    def __init__(
        self,
        registry=None,
        event_bus=None
    ):

        self.system = (
            "GENESIS AGENT HARNESS v1"
        )

        self.registry = registry

        self.event_bus = event_bus

        self.running_agents = {}



    def register(
        self,
        agent
    ):

        self.running_agents[
            agent.name
        ] = agent


        if self.registry:

            self.registry.register_agent(
                agent.name,
                agent.capabilities
            )


        if self.event_bus:

            self.event_bus.publish(
                "AGENT_REGISTERED",
                {
                    "agent":
                        agent.name
                }
            )


        return {

            "agent":
                agent.name,

            "status":
                "CONNECTED",

            "timestamp":
                time.time()

        }



    def execute(
        self,
        mission
    ):

        results = []


        for agent in self.running_agents.values():

            if hasattr(
                agent,
                "execute"
            ):

                results.append(

                    agent.execute(
                        mission
                    )

                )


        if self.event_bus:

            self.event_bus.publish(
                "MISSION_COMPLETE",
                {
                    "mission":
                        mission,

                    "results":
                        len(results)
                }
            )


        return {

            "id":
                "mission_" +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "results":
                results,

            "status":
                "COMPLETE"

        }



    def report(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.running_agents),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_agent_harness = GenesisAgentHarness()
