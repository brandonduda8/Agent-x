import os
import json
import time
import uuid


class GenesisKnowledgeIngestionPipeline:

    def __init__(self):

        self.system = (
            "GENESIS KNOWLEDGE INGESTION PIPELINE v1"
        )

        self.storage = (
            "data/genesis_knowledge/knowledge_vault.json"
        )

        os.makedirs(
            "data/genesis_knowledge",
            exist_ok=True
        )

        if not os.path.exists(self.storage):

            with open(self.storage, "w") as f:
                json.dump([], f)



    def ingest(
        self,
        source_type,
        title,
        content
    ):

        entry = {

            "id":
                "knowledge_" +
                uuid.uuid4().hex[:8],

            "source_type":
                source_type,

            "title":
                title,

            "content":
                content,

            "timestamp":
                time.time(),

            "status":
                "AVAILABLE"
        }


        with open(self.storage, "r") as f:
            memory = json.load(f)


        memory.append(entry)


        with open(self.storage, "w") as f:
            json.dump(
                memory,
                f,
                indent=2
            )


        print(
            "📚 Knowledge ingested:",
            title
        )


        return entry



    def search(self, query):

        with open(self.storage, "r") as f:
            memory = json.load(f)


        results = []


        for item in memory:

            text = (
                item["title"] +
                " " +
                item["content"]
            ).lower()


            if query.lower() in text:

                results.append(item)


        return results



    def report(self):

        with open(self.storage, "r") as f:
            memory = json.load(f)


        return {

            "system":
                self.system,

            "knowledge_entries":
                len(memory),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_knowledge_ingestion_pipeline = (
    GenesisKnowledgeIngestionPipeline()
)
