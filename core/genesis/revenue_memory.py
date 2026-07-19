import json
import os
import time


class GenesisRevenueMemory:

    def __init__(self):
        self.path = "data/revenue_memory.json"
        os.makedirs("data", exist_ok=True)
        self.memory = self.load()


    def load(self):

        if os.path.exists(self.path):

            try:
                with open(self.path, "r") as f:
                    return json.load(f)

            except:
                pass

        return {
            "products": [],
            "checkouts": [],
            "sales": []
        }


    def save(self):

        with open(self.path, "w") as f:
            json.dump(
                self.memory,
                f,
                indent=2
            )


    def save_product(self, product):

        self.memory["products"].append(
            {
                "data": product,
                "timestamp": time.time()
            }
        )

        self.save()


    def save_checkout(self, checkout):

        self.memory["checkouts"].append(
            {
                "data": checkout,
                "timestamp": time.time()
            }
        )

        self.save()


    def report(self):

        return {
            "system": "GENESIS REVENUE MEMORY v1",
            "products":
                len(self.memory["products"]),
            "checkouts":
                len(self.memory["checkouts"]),
            "sales":
                len(self.memory["sales"]),
            "timestamp":
                time.time()
        }


revenue_memory = GenesisRevenueMemory()
