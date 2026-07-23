import time


class GenesisOutreachPipeline:


    def __init__(self):

        self.leads = []

        self.system = (
            "GENESIS OUTREACH PIPELINE v1"
        )


    def add(
        self,
        outreach
    ):

        lead = {

            "business":
                outreach["business"],

            "message":
                outreach["message"],

            "stage":
                "MESSAGE_CREATED",

            "timestamp":
                time.time()

        }


        self.leads.append(
            lead
        )


        return lead


    def status(self):

        return self.leads
