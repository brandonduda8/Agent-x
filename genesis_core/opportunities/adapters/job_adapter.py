from genesis_core.opportunities.adapters.base_adapter import GenesisOpportunityAdapter


class GenesisJobAdapter(
    GenesisOpportunityAdapter
):


    def __init__(self):

        super().__init__(

            "Remote Job Intelligence",

            "employment"

        )



    def scan(self):

        return [

            self.create_opportunity(

                "AI Data Specialist",

                "Remote AI data and evaluation work",

                500,

                "Prepare application"

            ),

            self.create_opportunity(

                "AI Automation Assistant",

                "Remote automation support role",

                1000,

                "Submit application"

            )

        ]
