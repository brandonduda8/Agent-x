import time
import uuid


class GenesisAdapterRegistry:


    def __init__(self):

        self.adapters = []



    def register(
        self,
        name,
        adapter_type,
        capabilities,
        status="READY"
    ):

        adapter = {

            "id":
            "adapter_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "type":
            adapter_type,

            "capabilities":
            capabilities,

            "status":
            status,

            "timestamp":
            time.time()

        }


        self.adapters.append(adapter)

        return adapter



    def list_all(self):

        return self.adapters



    def find(
        self,
        name
    ):

        for adapter in self.adapters:

            if adapter["name"] == name:

                return adapter


        return None
