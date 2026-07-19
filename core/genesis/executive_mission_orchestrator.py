import time
import uuid

from core.genesis.mission_intelligence_router import (
    mission_intelligence_router
)

from core.genesis.agent_matching_engine import (
    agent_matching_engine
)

from core.genesis.workforce_orchestrator import (
    workforce_orchestrator
)


class GenesisExecutiveMissionOrchestrator:

    def __init__(self):

        self.system = "GENESIS EXECUTIVE MISSION ORCHESTRATOR v2"

        self.missions = []



    def register_workforce_agents(
        self,
        workforce
    ):

        for agent in workforce.get(
            "agents",
            []
        ):

            agent_matching_engine.register_agent(
                agent["name"],
                agent["skills"]
            )



    def get_available_skills(self):

        skills = []

        for agent in agent_matching_engine.agents.values():

            skills.extend(
                agent["skills"]
            )

        return list(
            set(skills)
        )



    def create_mission(
        self,
        objective
    ):

        print(
            f"🎯 Creating executive mission: {objective}"
        )


        plan = mission_intelligence_router.route(
            objective
        )


        available_skills = self.get_available_skills()


        workforce = workforce_orchestrator.create_workforce(
            plan["id"],
            plan["required_capabilities"],
            available_skills
        )


        self.register_workforce_agents(
            workforce
        )


        team = agent_matching_engine.match(
            plan
        )


        mission = {

            "id":
                "executive_mission_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "plan":
                plan,

            "workforce":
                workforce,

            "team":
                team,

            "status":
                "READY",

            "created":
                time.time()
        }


        self.missions.append(
            mission
        )


        print(
            "🚀 Executive mission ready"
        )


        return mission



    def status(self):

        return {

            "system":
                self.system,

            "missions":
                len(self.missions),

            "timestamp":
                time.time()
        }



executive_mission_orchestrator = GenesisExecutiveMissionOrchestrator()
