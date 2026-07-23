import time
import uuid


class GenesisSystemRegistry:


    def __init__(self):

        self.systems = []



    def register_system(
        self,
        name,
        system_type,
        capabilities
    ):

        system = {

            "id":
            "system_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "type":
            system_type,

            "capabilities":
            capabilities,

            "status":
            "CONNECTED",

            "timestamp":
            time.time()

        }


        self.systems.append(system)

        return system



    def list_systems(self):

        return self.systems
