import time
import uuid


class GenesisRevenueEngine:


    def __init__(self):

        self.pipeline = []



    def create_lead(
        self,
        opportunity
    ):

        lead = {

            "id":
            "lead_" + uuid.uuid4().hex[:8],

            "name":
            opportunity.get("title"),

            "value":
            opportunity.get(
                "estimated_value",
                0
            ),

            "stage":
            "NEW",

            "created":
            time.time()

        }


        self.pipeline.append(
            lead
        )


        return lead



    def update_stage(
        self,
        lead_id,
        stage
    ):

        for lead in self.pipeline:

            if lead["id"] == lead_id:

                lead["stage"] = stage

                lead["updated"] = time.time()

                return lead


        return None



    def report(
        self
    ):

        total = sum(

            lead["value"]

            for lead in self.pipeline

        )


        return {

            "system":
            "GENESIS REVENUE INTELLIGENCE ENGINE v1",

            "pipeline_value":
            total,

            "leads":
            len(self.pipeline),

            "pipeline":
            self.pipeline

        }
