import json
import os
import time
import uuid


class GenesisKnowledgeDatabase:

    def __init__(self):

        self.system = "GENESIS KNOWLEDGE DATABASE v1"

        self.file = "data/genesis_intelligence.json"

        self.nodes = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                data = json.load(
                    open(self.file)
                )

                self.nodes = data.get(
                    "knowledge",
                    []
                )

            except:

                self.nodes = []


    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        json.dump(
            {
                "knowledge": self.nodes,
                "updated": time.time()
            },
            open(self.file,"w"),
            indent=4
        )


    def add_knowledge(
        self,
        topic,
        category,
        skills,
        source
    ):

        node = {

            "id":
                "knowledge_" +
                uuid.uuid4().hex[:8],

            "topic":
                topic,

            "category":
                category,

            "skills":
                skills,

            "source":
                source,

            "confidence":
                0.5,

            "created":
                time.time()

        }


        self.nodes.append(node)

        self.save()

        return node


    def search(
        self,
        skill
    ):

        return [

            n for n in self.nodes

            if skill in n.get(
                "skills",
                []
            )

        ]


    def report(self):

        return {

            "system":
                self.system,

            "knowledge_nodes":
                len(self.nodes),

            "timestamp":
                time.time()

        }


knowledge_database = GenesisKnowledgeDatabase()
