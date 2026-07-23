from genesis_core.opportunities.adapters.base_adapter import GenesisOpportunityAdapter


class GenesisBusinessAdapter(
    GenesisOpportunityAdapter
):


    def __init__(self):

        super().__init__(

            "Business Intelligence",

            "business"

        )



    def scan(self):

        return [

            self.create_opportunity(

                "Dental AI Reception Automation",

                "Businesses losing revenue from missed calls",

                999,

                "Create outreach mission"

            )

        ]
