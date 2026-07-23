import time


class GenesisStateSync:


    def __init__(
        self,
        crm=None,
        revenue=None,
        economic=None
    ):

        self.system = (
            "GENESIS STATE SYNCHRONIZATION ENGINE v1"
        )

        self.crm = crm
        self.revenue = revenue
        self.economic = economic



    def sync(self):

        result = {

            "system":
                self.system,

            "timestamp":
                time.time(),

            "synced": {}

        }


        if self.crm:

            try:

                leads = self.crm.pipeline()

                result["synced"]["crm"] = len(
                    leads.get("leads", [])
                )

            except Exception as e:

                result["synced"]["crm_error"] = str(e)



        if self.revenue:

            try:

                result["synced"]["revenue_pipeline"] = (
                    len(
                        self.revenue.pipeline
                    )
                )

            except Exception as e:

                result["synced"]["revenue_error"] = str(e)



        if self.economic:

            try:

                result["synced"]["opportunities"] = (
                    len(
                        self.economic.opportunities
                    )
                )

            except Exception as e:

                result["synced"]["economic_error"] = str(e)



        return result



genesis_state_sync = GenesisStateSync()
