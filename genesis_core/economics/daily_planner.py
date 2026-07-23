import time


class GenesisEconomicPlanner:


    def create_plan(
        self,
        ranked_opportunities
    ):

        ranked = sorted(

            ranked_opportunities,

            key=lambda x: x["score"],

            reverse=True

        )


        actions = []


        for item in ranked[:3]:

            actions.append({

                "focus":
                item["opportunity"],

                "priority":
                item["priority"],

                "action":
                "Create mission"

            })


        return {

            "system":
            "GENESIS DAILY ECONOMIC PLANNER v1",

            "actions":
            actions,

            "timestamp":
            time.time()

        }
