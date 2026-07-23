import time


class GenesisStateHydrator:


    def __init__(
        self,
        database=None
    ):

        self.system = (
            "GENESIS STATE HYDRATOR v1"
        )

        self.database = database



    def hydrate(
        self,
        economic,
        revenue
    ):

        result = {

            "system":
            self.system,

            "hydrated":
            [],

            "timestamp":
            time.time()

        }


        if not self.database:
            return result


        try:

            leads = self.database.query(
                "leads"
            )


            for lead in leads:

                value = float(
                    lead[5]
                )


                revenue.pipeline.append(
                    {
                        "id":
                        f"memory_{lead[0]}",

                        "name":
                        lead[1],

                        "value":
                        value,

                        "stage":
                        lead[4],

                        "created":
                        lead[6]
                    }
                )


                economic.opportunities.append(
                    {
                        "id":
                        f"memory_{lead[0]}",

                        "name":
                        lead[1],

                        "category":
                        lead[2],

                        "value":
                        value,

                        "status":
                        lead[4],

                        "timestamp":
                        lead[6]
                    }
                )


            result["hydrated"].append(
                {
                    "source":
                    "leads",

                    "records":
                    len(leads)
                }
            )


        except Exception as e:

            result["error"] = str(e)


        return result



genesis_state_hydrator = GenesisStateHydrator()
