import time
import uuid


class GenesisJobIntelligence:


    def __init__(self):

        self.opportunities = []



    def add_opportunity(
        self,
        title,
        category,
        source,
        estimated_value,
        action
    ):

        opportunity = {

            "id":
            "opp_" + uuid.uuid4().hex[:8],

            "title":
            title,

            "category":
            category,

            "source":
            source,

            "estimated_value":
            estimated_value,

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



    def rank(self):

        return sorted(

            self.opportunities,

            key=lambda x:
            x["estimated_value"],

            reverse=True

        )
