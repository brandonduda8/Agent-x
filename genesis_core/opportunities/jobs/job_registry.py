import time
import uuid


class GenesisJobRegistry:


    def __init__(self):

        self.sources = []


    def register_source(
        self,
        name,
        category,
        capabilities
    ):

        source = {

            "id":
            "job_source_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "capabilities":
            capabilities,

            "status":
            "READY",

            "timestamp":
            time.time()

        }


        self.sources.append(source)

        return source



    def list_sources(self):

        return self.sources
