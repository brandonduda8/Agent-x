import time


class GenesisRealWorldActionFabric:


    def __init__(
        self,
        registry,
        router,
        executor
    ):

        self.registry = registry
        self.router = router
        self.executor = executor

        self.system = (
            "GENESIS REAL-WORLD ACTION FABRIC v1"
        )


    def connect(
        self,
        name,
        capabilities
    ):

        return self.registry.register(
            name,
            capabilities
        )


    def request_action(
        self,
        capability,
        action
    ):

        route = self.router.find(
            capability
        )


        return {

            "system":
                self.system,

            "route":
                route,

            "execution":
                self.executor.execute(
                    route["available_connectors"][0]
                    if route["available_connectors"]
                    else "NONE",
                    action
                ),

            "timestamp":
                time.time()

        }
