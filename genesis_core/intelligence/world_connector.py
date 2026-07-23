import time


class GenesisWorldIntelligence:


    def __init__(self):

        self.adapters = []



    def add_adapter(
        self,
        adapter
    ):

        self.adapters.append(
            adapter
        )



    def scan_world(self):

        opportunities = []


        for adapter in self.adapters:

            results = adapter.collect()

            opportunities.extend(
                results
            )


        return {

            "system":
            "GENESIS WORLD INTELLIGENCE CONNECTOR v1",

            "opportunities":
            opportunities,

            "count":
            len(opportunities),

            "timestamp":
            time.time()

        }
