
class GenesisOpportunityIntelligence:


    def score(
        self,
        opportunity
    ):

        score = 0


        if opportunity["estimated_value"] >= 1000:

            score += 40


        if opportunity["category"] in [

            "AI Automation",

            "Employment",

            "Recurring Revenue"

        ]:

            score += 40


        if opportunity["stage"] == "NEW":

            score += 20



        return {

            "opportunity":
            opportunity["name"],

            "score":
            score,

            "priority":

            (

            "HIGH"

            if score >= 70

            else

            "MEDIUM"

            )

        }
