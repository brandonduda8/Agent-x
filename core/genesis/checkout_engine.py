import time

import stripe

from core.genesis.stripe_manager import stripe_manager
from core.genesis.revenue_memory import revenue_memory


class GenesisCheckoutEngine:

    def __init__(self):

        self.name = "GENESIS CHECKOUT ENGINE v2"
        self.history = []


    def create_checkout(self, price_id):

        print(
            f"🛒 Creating checkout for {price_id}"
        )

        if not stripe_manager.connected:

            raise Exception(
                "Stripe not connected"
            )


        session = stripe.checkout.Session.create(

            mode="payment",

            line_items=[
                {
                    "price": price_id,
                    "quantity": 1
                }
            ],

            success_url=
                "https://example.com/success",

            cancel_url=
                "https://example.com/cancel"

        )


        result = {

            "session_id":
                session.id,

            "checkout_url":
                session.url,

            "price_id":
                price_id,

            "timestamp":
                time.time()

        }


        self.history.append(result)


        revenue_memory.save_checkout(
            result
        )


        return result



    def report(self):

        return {

            "system":
                self.name,

            "stripe_connected":
                stripe_manager.connected,

            "checkouts_created":
                len(self.history),

            "memory":
                revenue_memory.report(),

            "timestamp":
                time.time()

        }



checkout_engine = GenesisCheckoutEngine()
