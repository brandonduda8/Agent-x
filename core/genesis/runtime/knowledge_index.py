import time


class GenesisKnowledgeIndex:


    def __init__(self):

        self.entries = []

        self.system = (
            "GENESIS KNOWLEDGE INDEX v1"
        )


    def add(
        self,
        title,
        domain,
        content
    ):


        entry = {

            "title":
                title,

            "domain":
                domain,

            "content":
                content,

            "timestamp":
                time.time()

        }


        self.entries.append(entry)


        return entry


    def all(self):

        return self.entries
