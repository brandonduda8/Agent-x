import time
import uuid


class GenesisLeadDatabase:


    def __init__(self):

        self.leads = {}


    def create(
        self,
        business,
        opportunity
    ):

        lead_id = (
            "lead_" +
            uuid.uuid4().hex[:8]
        )


        self.leads[lead_id] = {

            "id":
                lead_id,

            "business":
                business,

            "opportunity":
                opportunity,

            "status":
                "NEW",

            "timestamp":
                time.time()

        }


        return self.leads[lead_id]


    def all(self):

        return self.leads
