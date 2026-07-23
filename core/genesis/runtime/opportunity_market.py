import time
import uuid


class GenesisOpportunityMarket:


    def __init__(self):

        self.opportunities = []


    def create(
        self,
        business,
        problem,
        solution,
        value
    ):

        opportunity = {

            "id":
                "opportunity_" +
                uuid.uuid4().hex[:8],

            "business":
                business,

            "problem":
                problem,

            "solution":
                solution,

            "value":
                value,

            "status":
                "AVAILABLE",

            "timestamp":
                time.time()

        }


        self.opportunities.append(opportunity)

        return opportunity
