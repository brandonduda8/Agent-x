import time


class GenesisRuntimeRegistry:


    def __init__(self):

        self.system = (
            "GENESIS RUNTIME REGISTRY v1"
        )

        self.services = {}



    def register(
        self,
        name,
        service
    ):

        self.services[name] = service

        print(
            f"🔗 Runtime Connected: {name}"
        )

        return service



    def get(
        self,
        name
    ):

        return self.services.get(name)



    def has(
        self,
        name
    ):

        return name in self.services



    def report(self):

        return {

            "system":
            self.system,

            "services":
            list(
                self.services.keys()
            ),

            "count":
            len(
                self.services
            ),

            "timestamp":
            time.time()

        }



runtime_registry = GenesisRuntimeRegistry()
