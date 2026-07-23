import time
import uuid


class GenesisWorldConnector:


    def __init__(self):

        self.sources = []

        self.opportunities = []



    def register_source(
        self,
        name,
        category
    ):

        source = {

            "id":
            "source_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "status":
            "CONNECTED",

            "timestamp":
            time.time()

        }


        self.sources.append(source)

        return source



    def ingest(
        self,
        source,
        title,
        description,
        value
    ):

        opportunity = {

            "id":
            "world_opp_" + uuid.uuid4().hex[:8],

            "source":
            source["name"],

            "category":
            source["category"],

            "name":
            title,

            "description":
            description,

            "value":
            value,

            "status":
            "NEW",

            "timestamp":
            time.time()

        }


        self.opportunities.append(
            opportunity
        )


        return opportunity



    def scan(self):

        return {

            "system":
            "GENESIS WORLD EXECUTION CONNECTOR v1",

            "sources":
            len(self.sources),

            "opportunities":
            len(self.opportunities),

            "timestamp":
            time.time()

        }
