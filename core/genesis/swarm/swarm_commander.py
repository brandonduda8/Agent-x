import time
import uuid

from core.genesis.swarm.agent_specialization_factory import (
    agent_specialization_factory
)

from core.genesis.swarm.swarm_matcher import (
    swarm_matcher
)


class GenesisSwarmCommander:


    def __init__(self):

        self.system = "GENESIS SWARM COMMANDER v1"
        self.cycles = []



    def create_swarm(self, objective):


        print(
            "⚡ Creating autonomous swarm:",
            objective
        )


        agents = []


        if "sales" in objective.lower():

            agents.append(
                agent_specialization_factory.create(
                    "Prospecting",
                    [
                        "research",
                        "lead_generation"
                    ]
                )
            )


            agents.append(
                agent_specialization_factory.create(
                    "Closing",
                    [
                        "sales",
                        "negotiation"
                    ]
                )
            )


        if "build" in objective.lower():

            agents.append(
                agent_specialization_factory.create(
                    "Engineering",
                    [
                        "coding",
                        "deployment"
                    ]
                )
            )


        if not agents:

            agents.append(
                agent_specialization_factory.create(
                    "General Intelligence",
                    [
                        "analysis",
                        "execution"
                    ]
                )
            )


        team = swarm_matcher.match(
            objective,
            agents
        )


        cycle = {

            "id":
            "swarm_cycle_" + uuid.uuid4().hex[:8],

            "objective":
            objective,

            "team":
            team,

            "status":
            "COMPLETE",

            "timestamp":
            time.time()

        }


        self.cycles.append(cycle)


        print(
            "🚀 Swarm created"
        )


        return cycle



    def report(self):

        return {

            "system":
            self.system,

            "cycles":
            len(self.cycles),

            "timestamp":
            time.time()

        }



swarm_commander = GenesisSwarmCommander()
