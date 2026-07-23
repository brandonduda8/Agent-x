import time
import uuid


class GenesisLeadPipeline:


    def __init__(self):

        self.leads = []



    def create_lead(
        self,
        business,
        industry,
        problem,
        offer,
        value
    ):

        lead = {

            "id":
            "lead_" + uuid.uuid4().hex[:8],

            "business":
            business,

            "industry":
            industry,

            "problem":
            problem,

            "offer":
            offer,

            "value":
            value,

            "stage":
            "NEW",

            "timestamp":
            time.time()

        }


        self.leads.append(lead)

        return lead



    def update_stage(
        self,
        lead_id,
        stage
    ):

        for lead in self.leads:

            if lead["id"] == lead_id:

                lead["stage"] = stage


        return self.leads



    def get_leads(self):

        return self.leads
