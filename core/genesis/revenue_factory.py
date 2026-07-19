import time

from core.genesis.stripe_manager import stripe_manager
from core.genesis.revenue_memory import revenue_memory


class GenesisRevenueFactory:

    def __init__(self):
        self.name = "GENESIS REVENUE FACTORY v2"
        self.history = []


    def build_product(self, idea):

        print(f"💰 Building revenue product: {idea}")

        tiers = [
            {
                "name": f"{idea} - Starter",
                "price": 29
            },
            {
                "name": f"{idea} - Professional",
                "price": 99
            },
            {
                "name": f"{idea} - Enterprise",
                "price": 299
            }
        ]


        products = []


        for tier in tiers:

            product = stripe_manager.create_product(
                tier["name"],
                f"{tier['name']} subscription",
                tier["price"]
            )

            products.append(product)


        result = {
            "idea": idea,
            "stripe_products": products,
            "timestamp": time.time()
        }


        self.history.append(result)


        try:
            revenue_memory.save_product(result)
        except Exception as e:
            print(
                f"⚠️ Revenue memory save skipped: {e}"
            )


        return result



    def report(self):

        return {
            "system": self.name,
            "products_created": len(self.history),
            "memory": revenue_memory.report(),
            "timestamp": time.time()
        }


revenue_factory = GenesisRevenueFactory()
