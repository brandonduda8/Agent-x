import time

from core.genesis.revenue_intelligence import revenue_intelligence
from core.genesis.revenue_factory import revenue_factory
from core.genesis.checkout_engine import checkout_engine
from core.genesis.landing_page_factory import landing_page_factory


class GenesisLaunchOrchestrator:

    def __init__(self):
        self.name = "GENESIS LAUNCH ORCHESTRATOR v2"
        self.history = []


    async def launch(self, idea):

        print("""
================================
🚀 GENESIS AUTONOMOUS LAUNCH
================================
""")

        print(f"🎯 Idea: {idea}")


        evaluation = revenue_intelligence.analyze(
            idea
        )


        if evaluation["recommendation"] != "BUILD":

            return {
                "status": "REJECTED",
                "evaluation": evaluation
            }


        print("🏭 Creating product...")


        product = revenue_factory.build_product(
            idea
        )


        print("🛒 Creating checkout links...")


        checkout_links = []


        for item in product["stripe_products"]:

            checkout = checkout_engine.create_checkout(
                item["price_id"]
            )

            checkout_links.append(
                checkout
            )


        primary_checkout = checkout_links[0]["checkout_url"]


        print("🌐 Creating landing page...")


        page = landing_page_factory.create_page(
            idea,
            f"Automate business tasks with {idea}",
            primary_checkout
        )


        result = {

            "idea": idea,

            "evaluation":
                evaluation,

            "product":
                product,

            "checkouts":
                checkout_links,

            "landing_page":
                page,

            "timestamp":
                time.time()

        }


        self.history.append(result)


        print("✅ LAUNCH COMPLETE")


        return result



    def report(self):

        return {

            "system":
                self.name,

            "launches":
                len(self.history),

            "timestamp":
                time.time()

        }



launch_orchestrator = GenesisLaunchOrchestrator()
