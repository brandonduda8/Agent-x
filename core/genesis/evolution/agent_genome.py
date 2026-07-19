import time
import uuid


class GenesisAgentGenome:

    def __init__(self):

        self.system = "GENESIS AGENT GENOME v1"

        self.genomes = {}



    def create_genome(
        self,
        agent,
        skills
    ):

        genome = {

            "id":
                "genome_" + uuid.uuid4().hex[:8],

            "agent":
                agent,

            "version":
                "1.0",

            "skills":
                skills,

            "upgrades":
                [],

            "evolution_count":
                0,

            "status":
                "INITIALIZED",

            "created":
                time.time()
        }


        self.genomes[agent] = genome


        print(
            f"🧬 Genome created: {agent}"
        )


        return genome



    def add_upgrade(
        self,
        agent,
        capability
    ):

        genome = self.genomes.get(agent)

        if not genome:
            return None


        genome["upgrades"].append(
            capability
        )

        genome["evolution_count"] += 1

        genome["version"] = (
            str(
                float(
                    genome["version"]
                ) + 1
            )
        )

        genome["status"] = "IMPROVED"


        print(
            f"⬆️ Agent upgraded: {agent}"
        )


        return genome



agent_genome = GenesisAgentGenome()
