import time


class GenesisActionRouter:


    def __init__(
        self,
        registry
    ):

        self.registry = registry

        self.system = "GENESIS ACTION ROUTER v1"



    def route(
        self,
        capability,
        task
    ):

        actions = self.registry.find_by_capability(
            capability
        )


        if not actions:

            return {

                "status": "NO_ACTION_AVAILABLE",

                "task": task

            }



        action = actions[0]


        return {

            "action": action,

            "task": task,

            "status": "ROUTED",

            "timestamp": time.time()

        }
