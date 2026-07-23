import time
import uuid


class GenesisOpportunityMarketplace:


    def __init__(self):

        self.opportunities = []


    def create(
        self,
        business,
        problem,
        solution
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

            "status":
                "NEW",

            "timestamp":
                time.time()

        }


        self.opportunities.append(
            opportunity
        )


        return opportunity


    def all(self):

        return self.opportunities
