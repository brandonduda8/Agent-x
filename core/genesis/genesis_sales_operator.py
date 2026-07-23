import time


from core.genesis.sales.offer_builder import (
    offer_builder
)

from core.genesis.sales.outreach_generator import (
    outreach_generator
)

from core.genesis.sales.followup_engine import (
    followup_engine
)

from core.genesis.sales.sales_analytics import (
    sales_analytics
)



class GenesisSalesOperator:


    def __init__(self):

        self.system = (
            "GENESIS AUTONOMOUS SALES OPERATOR v1"
        )



    def launch_campaign(
        self,
        company,
        market,
        problem,
        solution,
        price
    ):


        offer = offer_builder.create_offer(
            market,
            problem,
            solution,
            price
        )


        outreach = outreach_generator.generate(
            company,
            offer["solution"]
        )


        followup = followup_engine.create_sequence(
            company
        )


        sales_analytics.track(
            {
                "company":company,
                "offer":offer["id"]
            }
        )


        return {

            "offer":
            offer,

            "outreach":
            outreach,

            "followup":
            followup,

            "status":
            "CAMPAIGN_READY",

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "offer_system":
            offer_builder.report(),

            "outreach":
            outreach_generator.report(),

            "followup":
            followup_engine.report(),

            "analytics":
            sales_analytics.report(),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



genesis_sales_operator = GenesisSalesOperator()
