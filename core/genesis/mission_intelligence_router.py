import time


from core.genesis.agent_matching_engine import (
    agent_matching_engine
)


class GenesisMissionIntelligenceRouter:

    """
    GENESIS MISSION INTELLIGENCE ROUTER v3

    Converts objectives into:

    - required capabilities
    - dynamic agent teams
    - execution requirements
    """


    def __init__(self):

        self.system = (
            "GENESIS MISSION INTELLIGENCE ROUTER v3"
        )

        self.decisions = []


    def register_default_agents(self):

        if agent_matching_engine.agents:
            return


        agent_matching_engine.register_agent(
            "Research Agent",
            [
                "market_research",
                "lead_generation",
                "prospect_analysis"
            ]
        )


        agent_matching_engine.register_agent(
            "Revenue Agent",
            [
                "sales_pipeline",
                "outreach",
                "offer_creation"
            ]
        )


        agent_matching_engine.register_agent(
            "Automation Agent",
            [
                "workflow_automation",
                "process_design",
                "integration"
            ]
        )


        agent_matching_engine.register_agent(
            "Sales Agent",
            [
                "sales_pipeline",
                "outreach",
                "closing"
            ]
        )



    def analyze(
        self,
        objective
    ):


        self.register_default_agents()


        text = objective.lower()


        skills = []



        if any(word in text for word in [
            "client",
            "customer",
            "revenue",
            "sales",
            "business",
            "income",
            "automation"
        ]):

            skills.extend([

                "market_research",

                "lead_generation",

                "sales_pipeline",

                "outreach",

                "offer_creation"

            ])



        if any(word in text for word in [

            "automation",

            "workflow",

            "system",

            "process"

        ]):


            skills.append(
                "workflow_automation"
            )



        if any(word in text for word in [

            "app",

            "software",

            "platform",

            "code",

            "build"

        ]):


            skills.append(
                "software_creation"
            )



        if not skills:

            skills.append(
                "market_research"
            )



        mission_preview = {

            "id":
                f"mission_{int(time.time())}",

            "required_capabilities":
                list(set(skills))

        }



        match = (

            agent_matching_engine
            .match(
                mission_preview
            )

        )



        team = match.get(
            "team",
            []
        )



        decision = {


            "id":
                f"decision_{int(time.time())}",


            "objective":
                objective,


            "assigned_agents":
                [
                    member["agent"]
                    for member in team
                ],


            "team":
                team,


            "required_skills":
                    list(set(skills)),
                    "required_capabilities":
                    list(set(skills)),


            "priority":
                10,


            "status":
                "READY",


            "created":
                time.time()

        }



        self.decisions.append(
            decision
        )



        print(
            "🧠 Mission Intelligence:"
        )


        for member in team:

            print(

                f"   🤖 {member['agent']} -> "
                f"{member['matched_skills']}"

            )


        return decision



    def route(self, objective):
        return self.analyze(objective)

    def status(self):

        return {

            "system":
                self.system,

            "decisions":
                len(self.decisions),

            "timestamp":
                time.time()

        }



mission_intelligence_router = (
    GenesisMissionIntelligenceRouter()
)
