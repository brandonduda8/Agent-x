import uuid
import time


class GenesisIntelligenceGraph:

    def __init__(self):
        self.system = "GENESIS INTELLIGENCE GRAPH v1"
        self.nodes = []

    def add_node(self, node_type, name, data=None):

        node = {
            "id": "node_" + uuid.uuid4().hex[:8],
            "type": node_type,
            "name": name,
            "data": data or {},
            "created": time.time()
        }

        self.nodes.append(node)

        print(f"🧠 Intelligence node created: {name}")

        return node


    def search(self, name):

        return [
            node
            for node in self.nodes
            if name.lower() in node["name"].lower()
        ]


    def report(self):

        return {
            "system": self.system,
            "nodes": len(self.nodes),
            "timestamp": time.time()
        }


intelligence_graph = GenesisIntelligenceGraph()
