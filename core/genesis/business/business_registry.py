import time
import uuid


class GenesisBusinessRegistry:

    def __init__(self):

        self.system = "GENESIS BUSINESS REGISTRY v1"
        self.businesses = []


    def register_business(
        self,
        name,
        market,
        opportunity_value,
        agents
    ):

        business = {

            "id":
            "business_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "market":
            market,

            "estimated_value":
            opportunity_value,

            "agents":
            agents,

            "revenue":
            0,

            "status":
            "ACTIVE",

            "created":
            time.time()

        }


        self.businesses.append(
            business
        )


        print(
            f"🏢 Business registered: {name}"
        )


        return business



    def list_businesses(self):

        return self.businesses



    def report(self):

        return {

            "system":
            self.system,

            "businesses":
            len(self.businesses),

            "timestamp":
            time.time()

        }



business_registry = GenesisBusinessRegistry()
