import time
import uuid


class GenesisBusinessProfiles:


    def __init__(self):

        self.businesses = {}


    def register(
        self,
        name,
        industry,
        needs
    ):

        business_id = (
            "business_" +
            uuid.uuid4().hex[:8]
        )


        profile = {

            "id":
                business_id,

            "name":
                name,

            "industry":
                industry,

            "needs":
                needs,

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }


        self.businesses[business_id] = profile


        return profile


    def all(self):

        return self.businesses
