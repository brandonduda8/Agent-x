class GenesisGlobalOpportunityScanner:


    def scan(
        self,
        registry
    ):

        opportunities = registry.all()


        ranked = sorted(

            opportunities,

            key=lambda x:
            x.get(
                "estimated_value",
                0
            ),

            reverse=True

        )


        return ranked
