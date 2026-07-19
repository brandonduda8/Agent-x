import os
import time

from dotenv import load_dotenv

load_dotenv()

try:
    import stripe
except ImportError:
    stripe = None


class GenesisStripeManager:

    def __init__(self):
        self.name = "GENESIS STRIPE MANAGER v1"
        self.connected = False
        self.products = []
        self.connect()


    def connect(self):

        key = os.getenv("STRIPE_SECRET_KEY")

        if not key:
            print("⚠️ STRIPE_SECRET_KEY missing")
            return False

        if stripe is None:
            print("⚠️ Stripe package missing")
            return False

        stripe.api_key = key

        try:
            stripe.Account.retrieve()

            self.connected = True

            print("💳 Stripe connected")

        except Exception as e:

            print(
                f"⚠️ Stripe connection failed: {e}"
            )

        return self.connected


    def create_product(
        self,
        name,
        description,
        price
    ):

        if not self.connected:

            return {
                "error": "Stripe not connected"
            }


        product = stripe.Product.create(
            name=name,
            description=description
        )


        stripe_price = stripe.Price.create(
            product=product.id,
            unit_amount=int(price * 100),
            currency="usd"
        )


        result = {

            "product_id": product.id,

            "price_id": stripe_price.id,

            "name": name,

            "price": price,

            "timestamp": time.time()

        }


        self.products.append(result)


        return result



    def report(self):

        return {

            "system": self.name,

            "connected": self.connected,

            "products_created": len(self.products),

            "timestamp": time.time()

        }



stripe_manager = GenesisStripeManager()
