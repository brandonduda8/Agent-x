import time


class GenesisRevenueOperations:


    def create_strategy(
        self,
        offer
    ):

        return {

            "revenue_model":

            {

                "setup_fee":
                    offer["pricing"]["setup"],

                "recurring":
                    offer["pricing"]["monthly"]

            },


            "growth_actions":

            [

                "Generate leads",

                "Close customers",

                "Increase retention"

            ],


            "timestamp":
                time.time()

        }
