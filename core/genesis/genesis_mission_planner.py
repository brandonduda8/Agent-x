import time
import uuid


class GenesisMissionPlanner:

    def __init__(self):

        self.name = "GENESIS MISSION PLANNER v1"


    def classify_mission(self, objective):

        objective_lower = objective.lower()

        agents = []

        if any(word in objective_lower for word in [
            "revenue",
            "sales",
            "money",
            "business",
            "customers",
            "market"
        ]):

            agents.extend([
                "Genesis Market Research Agent",
                "Genesis Product Discovery Agent",
                "Genesis Offer Builder Agent",
                "Genesis Outreach Agent",
                "Genesis Analytics Agent"
            ])


        if any(word in objective_lower for word in [
            "software",
            "app",
            "system",
            "automation",
            "code"
        ]):

            agents.extend([
                "Genesis Computer Science Architect Agent",
                "Genesis Software Engineer Agent",
                "Genesis AI Engineer Agent",
                "Genesis QA Scientist Agent"
            ])


        if any(word in objective_lower for word in [
            "local",
            "business",
            "seo",
            "leads"
        ]):

            agents.append(
                "Genesis Local Business Intelligence Agent"
            )


        if not agents:

            agents.append(
                "Genesis Computer Science Architect Agent"
            )


        return list(
            dict.fromkeys(
                agents
            )
        )



    def create_task_graph(
        self,
        objective
    ):

        selected_agents = self.classify_mission(
            objective
        )

        tasks = []


        for agent in selected_agents:

            tasks.append(
                {

                    "id":
                        "task_" +
                        uuid.uuid4().hex[:8],

                    "agent":
                        agent,

                    "objective":
                        objective,

                    "status":
                        "PLANNED",

                    "created":
                        time.time()

                }
            )


        return {

            "id":
                "mission_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "agents_selected":
                selected_agents,

            "tasks":
                tasks,

            "status":
                "READY",

            "created":
                time.time()

        }



    def get_status(self):

        return {

            "system":
                self.name,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_mission_planner = GenesisMissionPlanner()
