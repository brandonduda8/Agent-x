class GenesisAgentModelManager:


    def __init__(
        self,
        router,
        registry
    ):

        self.router = router

        self.models = registry.list_models()



    def assign(
        self,
        agent,
        capability
    ):

        model = self.router.route(

            capability,

            self.models

        )


        return {

            "agent":
            agent,

            "capability":
            capability,

            "model":
            model["name"],

            "provider":
            model.get(
                "provider",
                "unknown"
            ),

            "tier":
            model.get(
                "tier",
                "unknown"
            )

        }
