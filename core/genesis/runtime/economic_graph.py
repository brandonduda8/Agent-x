import time


class GenesisEconomicGraph:


    def __init__(self):

        self.nodes = []
        self.connections = []


    def add_node(
        self,
        node
    ):

        self.nodes.append(node)

        return node


    def connect(
        self,
        source,
        target,
        relationship
    ):

        self.connections.append({

            "source":
                source,

            "target":
                target,

            "relationship":
                relationship,

            "timestamp":
                time.time()

        })


    def view(self):

        return {

            "nodes":
                self.nodes,

            "connections":
                self.connections

        }
