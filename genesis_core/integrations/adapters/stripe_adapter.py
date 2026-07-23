import os


class StripeAdapter:


    def check(self):

        key = os.getenv(
            "STRIPE_SECRET_KEY"
        )


        if key:

            return {

                "name":
                "Stripe",

                "status":
                "CONFIGURED"

            }


        return {

            "name":
            "Stripe",

            "status":
            "MISSING_KEY"

        }
