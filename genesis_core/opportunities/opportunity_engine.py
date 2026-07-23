from genesis_core.opportunities.adapters.job_adapter import GenesisJobAdapter
from genesis_core.opportunities.adapters.business_adapter import GenesisBusinessAdapter


class GenesisOpportunityEngine:


    def __init__(self):

        self.adapters = [

            GenesisJobAdapter(),

            GenesisBusinessAdapter()

        ]



    def discover(self):

        opportunities = []


        for adapter in self.adapters:

            opportunities.extend(

                adapter.scan()

            )


        return sorted(

            opportunities,

            key=lambda x:
            x["estimated_value"],

            reverse=True

        )
