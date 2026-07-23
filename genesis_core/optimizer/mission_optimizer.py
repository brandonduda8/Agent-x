import time
import uuid


class GenesisMissionOptimizer:


    def __init__(self):

        self.missions = []



    def score_opportunity(
        self,
        opportunity
    ):

        revenue = opportunity.get(
            "value",
            0
        )


        urgency = opportunity.get(
            "urgency",
            50
        )


        automation_fit = opportunity.get(
            "automation_fit",
            50
        )


        speed = opportunity.get(
            "speed",
            50
        )


        score = (

            min(revenue / 10, 40)

            +

            urgency * .25

            +

            automation_fit * .2

            +

            speed * .15

        )


        return round(
            score,
            2
        )



    def create_mission(
        self,
        opportunity
    ):


        score = self.score_opportunity(
            opportunity
        )


        mission = {


            "id":
            "mission_" + uuid.uuid4().hex[:8],


            "objective":
            opportunity["name"],


            "value":
            opportunity.get(
                "value",
                0
            ),


            "priority":

            "EXECUTE"

            if score >= 70

            else

            "REVIEW",


            "score":
            score,


            "tasks":

            [

            "Research opportunity",

            "Create execution plan",

            "Assign agents",

            "Track outcome"

            ],


            "status":
            "READY",


            "timestamp":
            time.time()

        }


        self.missions.append(
            mission
        )


        return mission



    def best_mission(
        self
    ):

        if not self.missions:

            return None


        return sorted(

            self.missions,

            key=lambda x:
            x["score"],

            reverse=True

        )[0]



    def status(self):

        return {

            "system":
            "GENESIS AUTONOMOUS MISSION OPTIMIZER v1",

            "missions":
            len(self.missions),

            "timestamp":
            time.time()

        }
