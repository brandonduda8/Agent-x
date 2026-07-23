import json
import os
import time
import uuid


class GenesisIntelligenceGraph:

    def __init__(self):

        self.system = "GENESIS INTELLIGENCE GRAPH v1"

        self.file = "data/genesis_intelligence_graph.json"

        self.nodes = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                self.nodes = json.load(
                    open(self.file)
                )

            except:

                self.nodes = []


    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        json.dump(
            self.nodes,
            open(self.file,"w"),
            indent=4
        )


    def add_node(
        self,
        node_type,
        name,
        data=None
    ):

        node = {

            "id":
                "node_" +
                uuid.uuid4().hex[:8],

            "type":
                node_type,

            "name":
                name,

            "data":
                data or {},

            "created":
                time.time()

        }


        self.nodes.append(node)

        self.save()

        return node


    def search(
        self,
        name
    ):

        return [

            n for n in self.nodes

            if name.lower()
            in n["name"].lower()

        ]


    def report(self):

        return {

            "system":
                self.system,

            "nodes":
                len(self.nodes),

            "timestamp":
                time.time()

        }


intelligence_graph = GenesisIntelligenceGraph()
