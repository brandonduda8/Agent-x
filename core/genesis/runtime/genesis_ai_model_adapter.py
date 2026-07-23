import time


class GenesisAIModelAdapter:


    def __init__(
        self,
        registry,
        router,
        requests
    ):

        self.registry = registry
        self.router = router
        self.requests = requests

        self.system = (
            "GENESIS AI MODEL ADAPTER v1"
        )


    def connect_model(
        self,
        name,
        capabilities
    ):

        return self.registry.register(
            name,
            capabilities
        )


    def request(
        self,
        capability,
        prompt
    ):

        route = self.router.route(
            capability
        )


        model = (
            route["models"][0]
            if route["models"]
            else "NONE"
        )


        return {

            "system":
                self.system,

            "route":
                route,

            "request":
                self.requests.create(
                    model,
                    prompt
                ),

            "timestamp":
                time.time()

        }
