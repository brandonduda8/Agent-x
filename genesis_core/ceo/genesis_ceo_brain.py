import time
import uuid


class GenesisCEOBrian:

    def __init__(self):

        self.system = (
            "GENESIS CEO BRAIN v1"
        )

        self.decisions = []


    def evaluate_opportunities(
        self,
        opportunities
    ):

        scored = []

        for opportunity in opportunities:

            value = opportunity.get(
                "value",
                0
            )

            category = opportunity.get(
                "category",
                "unknown"
            )


            score = value


            if category == "AI Automation":
                score += 50


            scored.append(
                {
                    "opportunity":
                    opportunity,

                    "score":
                    score,

                    "reason":
                    "Economic value and execution alignment"
                }
            )


        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return scored


    def make_decision(
        self,
        opportunities,
        agents
    ):

        ranked = (
            self.evaluate_opportunities(
                opportunities
            )
        )


        if not ranked:

            return {
                "system":
                self.system,

                "decision":
                "WAIT",

                "reason":
                "No opportunities available",

                "timestamp":
                time.time()
            }


        selected = ranked[0]


        decision = {

            "id":
            "decision_" +
            uuid.uuid4().hex[:8],


            "system":
            self.system,


            "decision":
            "EXECUTE",


            "priority":
            "HIGH",


            "mission":
            {

                "name":
                selected["opportunity"]["name"],


                "value":
                selected["opportunity"]["value"],


                "reason":
                selected["reason"]

            },


            "recommended_agents":
            agents,


            "next_action":
            "Create execution mission",


            "timestamp":
            time.time()

        }


        self.decisions.append(
            decision
        )


        return decision



    def report(self):

        return {

            "system":
            self.system,

            "decisions":
            len(self.decisions),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_ceo_brain = GenesisCEOBrian()
