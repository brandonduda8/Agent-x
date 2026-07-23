import time


class GenesisIntelligenceFabric:


    def __init__(
        self
    ):

        self.nodes = []



    def add(
        self,
        category,
        data
    ):

        node = {

            "category":
            category,

            "data":
            data,

            "timestamp":
            time.time()

        }


        self.nodes.append(
            node
        )


        return node



    def search(
        self,
        category
    ):

        return [

            node

            for node in self.nodes

            if node["category"] == category

        ]



    def status(
        self
    ):

        return {

            "system":
            "GENESIS INTELLIGENCE FABRIC v1",

            "nodes":
            len(self.nodes),

            "categories":

            list(

                set(

                    n["category"]

                    for n in self.nodes

                )

            )

        }
