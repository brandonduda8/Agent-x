import time
import uuid


class GenesisLeadGenerator:


    def __init__(self):

        self.system = "GENESIS LEAD GENERATOR v1"
        self.leads = []


    def generate(self, market):

        lead = {

            "id":
            "lead_" + uuid.uuid4().hex[:8],

            "market":
            market,

            "company_type":
            "Small Business",

            "need":
            "AI automation",

            "status":
            "NEW",

            "created":
            time.time()

        }


        self.leads.append(lead)


        print(
            "👤 Lead generated:",
            lead["id"]
        )


        return lead



    def report(self):

        return {

            "system":
            self.system,

            "leads":
            len(self.leads),

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



lead_generator = GenesisLeadGenerator()
