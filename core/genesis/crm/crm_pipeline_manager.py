import time


class GenesisCRMPipelineManager:


    def __init__(self):

        self.system = "GENESIS CRM PIPELINE v1"


        self.stages = [

            "NEW",
            "CONTACTED",
            "QUALIFIED",
            "OFFER_SENT",
            "NEGOTIATION",
            "WON",
            "REVENUE_TRACKED"

        ]


        self.pipeline = []



    def create_pipeline_item(
        self,
        contact,
        objective
    ):


        item = {

            "id":
            "pipeline_" + str(
                len(self.pipeline)+1
            ),

            "contact":
            contact,

            "objective":
            objective,

            "stage":
            "NEW",

            "created":
            time.time()

        }


        self.pipeline.append(item)


        return item



    def update_stage(
        self,
        pipeline_id,
        stage
    ):


        for item in self.pipeline:

            if item["id"] == pipeline_id:

                if stage in self.stages:

                    item["stage"] = stage


                return item



    def report(self):

        return {

            "system":
            self.system,

            "pipeline_items":
            len(self.pipeline),

            "stages":
            self.stages,

            "status":
            "ONLINE",

            "timestamp":
            time.time()

        }



crm_pipeline_manager = GenesisCRMPipelineManager()
