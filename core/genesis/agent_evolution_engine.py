import time
import uuid


class GenesisAgentEvolutionEngine:

    def __init__(self):

        self.system = "GENESIS AGENT EVOLUTION ENGINE v1"

        self.evolutions = []



    def evolve_agent(
        self,
        agent,
        skill
    ):

        evolution = {

            "id":
                "evolution_" + uuid.uuid4().hex[:8],

            "agent":
                agent,

            "new_skill":
                skill,

            "status":
                "EVOLVED",

            "timestamp":
                time.time()

        }


        self.evolutions.append(
            evolution
        )


        print(
            f"🧬 Agent evolved: {agent}"
        )


        return evolution



    def upgrade_capability(
        self,
        capability_graph,
        agent,
        skill
    ):

        capability = {

            "id":
                "cap_" + uuid.uuid4().hex[:8],

            "agent":
                agent,

            "capability":
                skill,

            "status":
                "AVAILABLE",

            "created":
                time.time()

        }


        capability_graph.append(
            capability
        )


        print(
            "🧠 Capability expanded"
        )


        return capability



    def evolve(
        self,
        agent,
        skill,
        capability_graph
    ):

        evolution = self.evolve_agent(
            agent,
            skill
        )


        capability = self.upgrade_capability(
            capability_graph,
            agent,
            skill
        )


        return {

            "evolution":
                evolution,

            "capability":
                capability

        }



    def report(self):

        return {

            "system":
                self.system,

            "evolutions":
                len(self.evolutions),

            "timestamp":
                time.time()

        }



agent_evolution_engine = GenesisAgentEvolutionEngine()
