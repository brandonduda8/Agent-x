import time
import uuid


class GenesisOpportunityDatabase:


    def __init__(self):

        self.opportunities = {}

        self.system = (
            "GENESIS OPPORTUNITY DATABASE v1"
        )


    def store(
        self,
        opportunity
    ):

        opp_id = (
            "opportunity_" +
            uuid.uuid4().hex[:8]
        )


        opportunity["id"] = opp_id

        opportunity["timestamp"] = time.time()


        self.opportunities[opp_id] = opportunity


        return opportunity


    def all(self):

        return self.opportunities
