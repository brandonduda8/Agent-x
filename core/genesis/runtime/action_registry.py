import time


class GenesisActionRegistry:


    def __init__(self):

        self.system = "GENESIS ACTION REGISTRY v1"

        self.actions = {}



    def register(
        self,
        name,
        handler,
        capability
    ):

        self.actions[name] = {

            "handler": handler,

            "capability": capability,

            "created": time.time()

        }


        return {

            "action": name,

            "status": "REGISTERED"

        }



    def get_actions(self):

        return list(
            self.actions.keys()
        )



    def find_by_capability(
        self,
        capability
    ):

        return [

            name

            for name, action
            in self.actions.items()

            if action["capability"] == capability

        ]
