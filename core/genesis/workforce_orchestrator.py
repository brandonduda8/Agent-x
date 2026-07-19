import time
import uuid

from core.genesis.autonomous_agent_factory import (
    autonomous_agent_factory
)

from core.genesis.workforce_intelligence import (
    workforce_intelligence
)


class GenesisWorkforceOrchestrator:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS WORKFORCE ORCHESTRATOR v2"

        self.missions = []



    def analyze_capabilities(
        self,
        required_skills,
        available_skills
    ):

        missing = []

        for skill in required_skills:

            if skill not in available_skills:

                missing.append(skill)

        return missing



    def create_missing_agents(
        self,
        missing_skills
    ):

        created = []

        for skill in missing_skills:

            existing = (
                workforce_intelligence
                .activate_existing(skill)
            )


            if existing:

                created.append(
                    existing
                )

                continue



            agent = (
                autonomous_agent_factory
                .spawn_from_capability_gap(
                    skill
                )
            )


            workforce_intelligence.remember_agent(
                {
                    "id":
                        agent["id"],

                    "name":
                        agent["name"],

                    "skills":
                        agent["skills"]
                }
            )


            created.append(
                agent
            )


        return created



    def create_workforce(
        self,
        mission,
        required_skills,
        available_skills
    ):


        missing = self.analyze_capabilities(
            required_skills,
            available_skills
        )


        agents = self.create_missing_agents(
            missing
        )


        workforce = {

            "id":
                "workforce_" +
                uuid.uuid4().hex[:8],

            "mission":
                mission,

            "required_skills":
                required_skills,

            "agents":
                agents,

            "status":
                "READY",

            "created":
                time.time()
        }


        self.missions.append(
            workforce
        )


        print(
            "🧬 Intelligent workforce assembled"
        )


        return workforce



    def report(self):

        return {

            "system":
                self.system,

            "workforces":
                len(self.missions),

            "timestamp":
                time.time()
        }



workforce_orchestrator = GenesisWorkforceOrchestrator()
