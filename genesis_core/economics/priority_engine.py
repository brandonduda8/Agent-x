import time


class GenesisPriorityEngine:


    def evaluate(
        self,
        opportunity
    ):

        score = 0

        factors = {}


        # Revenue potential
        value = opportunity.get(
            "estimated_value",
            0
        )

        if value >= 1000:
            factors["revenue"] = 40
        elif value >= 500:
            factors["revenue"] = 30
        else:
            factors["revenue"] = 15


        score += factors["revenue"]


        # Speed to income
        category = opportunity.get(
            "category",
            ""
        )

        if category in [
            "Employment",
            "AI Automation",
            "Freelance"
        ]:

            factors["speed"] = 25

        else:

            factors["speed"] = 10


        score += factors["speed"]


        # Problem urgency
        factors["urgency"] = 20

        score += factors["urgency"]


        # Automation fit
        if "AI" in opportunity.get(
            "name",
            ""
        ):

            factors["automation_fit"] = 15

        else:

            factors["automation_fit"] = 5


        score += factors["automation_fit"]



        priority = "EXECUTE"

        if score < 70:

            priority = "REVIEW"


        return {

            "system":
            "GENESIS ECONOMIC PRIORITY ENGINE v2",

            "opportunity":
            opportunity["name"],

            "score":
            score,

            "priority":
            priority,

            "breakdown":
            factors,

            "timestamp":
            time.time()

        }
