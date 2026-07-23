import uuid
import time


class GenesisBusinessRegistry:


    def __init__(self):

        self.businesses = []


    def register(
        self,
        name,
        industry,
        problem
    ):

        business = {

            "id":
                "business_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "industry":
                industry,

            "problem":
                problem,

            "timestamp":
                time.time()

        }


        self.businesses.append(business)

        return business
