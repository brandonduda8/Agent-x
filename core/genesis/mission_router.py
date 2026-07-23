import time
import uuid

from core.genesis.agent_matching_engine import (
    agent_matching_engine
)

from core.genesis.agent_registry import (
    agent_registry
)

from core.genesis.memory_engine import (
    memory_engine
)


class GenesisMissionRouter:


    def __init__(self):

        self.name = (
            "GENESIS MISSION ROUTER v1"
        )



    def analyze_skills(
        self,
        objective
    ):

        text = objective.lower()


        skills = []


        mapping = {

            "research":
                [
                    "market_research"
                ],

            "market":
                [
                    "market_research"
                ],

            "find":
                [
                    "lead_generation"
                ],

            "lead":
                [
                    "lead_generation"
                ],

            "sales":
                [
                    "sales_pipeline",
                    "outreach"
                ],

            "revenue":
                [
                    "sales_pipeline",
                    "offer_creation"
                ],

            "business":
                [
                    "offer_creation",
                    "sales_pipeline"
                ],

            "automation":
                [
                    "workflow_automation"
                ],

            "workflow":
                [
                    "workflow_automation"
                ],

            "build":
                [
                    "automation",
                    "development"
                ],

            "code":
                [
                    "development"
                ],

            "app":
                [
                    "development"
                ],

            "website":
                [
                    "development"
                ]

        }


        for keyword, capability in mapping.items():

            if keyword in text:

                for skill in capability:

                    if skill not in skills:

                        skills.append(skill)



        return skills



    def ensure_core_agents(self):


        if not agent_registry.get(
            "Research Agent"
        ):

            agent_matching_engine.register_agent(

                "Research Agent",

                "Market Research",

                [
                    "market_research",
                    "lead_generation"
                ]

            )


        if not agent_registry.get(
            "Revenue Agent"
        ):

            agent_matching_engine.register_agent(

                "Revenue Agent",

                "Sales",

                [
                    "sales_pipeline",
                    "offer_creation",
                    "outreach"
                ]

            )


        if not agent_registry.get(
            "Automation Agent"
        ):

            agent_matching_engine.register_agent(

                "Automation Agent",

                "Automation",

                [
                    "workflow_automation",
                    "automation"
                ]

            )


        if not agent_registry.get(
            "Builder Agent"
        ):

            agent_matching_engine.register_agent(

                "Builder Agent",

                "Development",

                [
                    "development"
                ]

            )



    def analyze(
        self,
        objective
    ):


        print(
            "🧠 Genesis Mission Intelligence"
        )


        self.ensure_core_agents()


        required_skills = (
            self.analyze_skills(
                objective
            )
        )


        mission = {

            "id":
                "mission_"
                + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "required_skills":
                required_skills,

            "status":
                "READY",

            "created":
                time.time()

        }



        team = (
            agent_matching_engine.match(
                mission
            )
        )



        mission["team"] = (
            team["team"]
        )


        mission["assigned_agents"] = [

            agent["agent"]

            for agent in team["team"]

        ]



        memory_engine.memory[
            "missions"
        ].append(
            mission
        )


        memory_engine.save()



        print(
            "🧬 Mission team:",
            mission["assigned_agents"]
        )


        return mission



mission_router = GenesisMissionRouter()
