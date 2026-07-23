import time


class GenesisKnowledgeRetriever:


    def __init__(
        self,
        index
    ):

        self.index = index

        self.system = (
            "GENESIS KNOWLEDGE RETRIEVER v1"
        )


    def search(
        self,
        topic
    ):


        results = []


        for entry in self.index.all():

            if (
                topic.lower()
                in entry["content"].lower()
                or
                topic.lower()
                in entry["domain"].lower()
            ):

                results.append(entry)


        return {

            "query":
                topic,

            "results":
                results,

            "timestamp":
                time.time()

        }
