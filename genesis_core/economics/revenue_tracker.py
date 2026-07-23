import time
import uuid


class GenesisRevenueTracker:


    def __init__(self):

        self.pipeline = []



    def create_opportunity(
        self,
        name,
        category,
        estimated_value
    ):

        opportunity = {

            "id":
            "revenue_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "estimated_value":
            estimated_value,

            "stage":
            "NEW",

            "timestamp":
            time.time()

        }


        self.pipeline.append(opportunity)

        return opportunity



    def update_stage(
        self,
        opportunity_id,
        stage
    ):

        for item in self.pipeline:

            if item["id"] == opportunity_id:

                item["stage"] = stage


        return self.pipeline



    def get_pipeline(self):

        return self.pipeline
