import time
import uuid


class GenesisEconomicMissionRouter:


    def __init__(self):

        self.missions = []



    def evaluate(
        self,
        opportunity
    ):

        value = opportunity.get(
            "estimated_value",
            0
        )


        category = opportunity.get(
            "category"
        )


        score = 0


        if value >= 900:
            score += 40

        elif value >= 500:
            score += 25


        if category == "business":
            score += 30

        if category == "employment":
            score += 20


        if "AI" in opportunity.get(
            "title",
            ""
        ):
            score += 20


        return score



    def create_mission(
        self,
        opportunity
    ):


        score = self.evaluate(
            opportunity
        )


        mission = {


            "id":
            "mission_" +
            uuid.uuid4().hex[:8],


            "objective":
            opportunity["title"],


            "source":
            opportunity["source"],


            "value":
            opportunity["estimated_value"],


            "priority":
            "EXECUTE"
            if score >= 70
            else
            "REVIEW",


            "score":
            score,


            "tasks":
            self.generate_tasks(
                opportunity
            ),


            "status":
            "READY",


            "created":
            time.time()

        }


        self.missions.append(
            mission
        )


        return mission



    def generate_tasks(
        self,
        opportunity
    ):


        if opportunity["category"] == "business":

            return [

                "Research decision maker",

                "Create outreach",

                "Follow up",

                "Close client"

            ]


        return [

            "Prepare application",

            "Customize resume",

            "Submit application",

            "Track response"

        ]



    def list_missions(self):

        return self.missions
