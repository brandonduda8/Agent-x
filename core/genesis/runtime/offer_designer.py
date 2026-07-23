import time


class GenesisOfferDesigner:


    def create(
        self,
        business
    ):

        return {

            "offer":

                business["business_name"],


            "pricing":

                {
                    "setup":
                        "$999",

                    "monthly":
                        "$299/month"
                },


            "services":

                [

                    "Automation setup",

                    "Lead recovery",

                    "Customer follow-up",

                    "Optimization"

                ],

            "timestamp":
                time.time()

        }
