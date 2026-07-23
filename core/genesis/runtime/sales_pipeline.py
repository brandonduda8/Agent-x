import time


class GenesisSalesPipeline:


    def __init__(self):

        self.pipeline = []


    def add(
        self,
        lead
    ):

        deal = {

            "lead":
                lead["id"],

            "stage":
                "PROSPECT",

            "value":
                999,

            "timestamp":
                time.time()

        }


        self.pipeline.append(deal)

        return deal


    def advance(
        self,
        lead_id,
        stage
    ):

        for deal in self.pipeline:

            if deal["lead"] == lead_id:

                deal["stage"] = stage


        return self.pipeline
