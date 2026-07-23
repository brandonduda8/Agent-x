import time
import uuid


class GenesisKnowledgeGraph:


    def __init__(self):

        self.nodes = []

        self.connections = []



    def add_node(
        self,
        node_type,
        name,
        data=None
    ):

        node = {

            "id":
            "node_" + uuid.uuid4().hex[:8],

            "type":
            node_type,

            "name":
            name,

            "data":
            data or {},

            "timestamp":
            time.time()

        }


        self.nodes.append(node)

        return node



    def connect(
        self,
        source,
        relationship,
        target
    ):

        connection = {

            "id":
            "edge_" + uuid.uuid4().hex[:8],

            "source":
            source["id"],

            "relationship":
            relationship,

            "target":
            target["id"],

            "timestamp":
            time.time()

        }


        self.connections.append(connection)

        return connection



    def find_connections(
        self,
        node_id
    ):

        return [

            edge

            for edge in self.connections

            if edge["source"] == node_id

            or edge["target"] == node_id

        ]



    def status(self):

        return {

            "system":
            "GENESIS KNOWLEDGE GRAPH FABRIC v1",

            "nodes":
            len(self.nodes),

            "connections":
            len(self.connections),

            "timestamp":
            time.time()

        }
