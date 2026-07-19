import time
import uuid


class GenesisKnowledgeGraph:

    def __init__(self):

        self.system = "GENESIS KNOWLEDGE GRAPH v1"

        self.knowledge = []


    def store(
        self,
        lesson
    ):

        node = {

            "id":
                "knowledge_" + uuid.uuid4().hex[:8],

            "lesson":
                lesson,

            "created":
                time.time()
        }


        self.knowledge.append(node)


        print(
            "🌐 Knowledge stored"
        )


        return node



    def search(
        self,
        keyword
    ):

        return [

            item for item in self.knowledge

            if keyword.lower()
            in str(item).lower()

        ]



    def report(self):

        return {

            "system":
                self.system,

            "knowledge_nodes":
                len(self.knowledge),

            "timestamp":
                time.time()
        }



knowledge_graph = GenesisKnowledgeGraph()
