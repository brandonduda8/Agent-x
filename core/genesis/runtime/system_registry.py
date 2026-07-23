import time


class GenesisSystemRegistry:


    def __init__(self):

        self.systems = {}


    def register(
        self,
        name,
        status
    ):

        self.systems[name] = {

            "name":
                name,

            "status":
                status,

            "timestamp":
                time.time()

        }


        return self.systems[name]


    def all(self):

        return self.systems
