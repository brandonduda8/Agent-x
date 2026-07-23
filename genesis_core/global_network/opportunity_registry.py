import time
import uuid


class GenesisOpportunityRegistry:


    def __init__(self):

        self.opportunities = []



    def add(
        self,
        name,
        category,
        source,
        value,
        problem="",
        action=""
    ):

        opportunity = {

            "id":
            "opp_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "source":
            source,

            "problem":
            problem,

            "estimated_value":
            value,

            "next_action":
            action,

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
