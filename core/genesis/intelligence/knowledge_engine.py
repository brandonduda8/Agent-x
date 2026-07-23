import time
import uuid


class GenesisKnowledgeEngine:

    def __init__(self):
        self.system = "GENESIS KNOWLEDGE ENGINE v1"
        self.knowledge = []


    def learn(self, topic, information):

        item = {
            "id": "knowledge_" + uuid.uuid4().hex[:8],
            "topic": topic,
            "information": information,
            "created": time.time()
        }

        self.knowledge.append(item)

        print(f"📚 Knowledge acquired: {topic}")

        return item


    def find(self, topic):

        return [
            item
            for item in self.knowledge
            if topic.lower() in item["topic"].lower()
        ]


    def report(self):

        return {
            "system": self.system,
            "knowledge_items": len(self.knowledge),
            "timestamp": time.time()
        }


knowledge_engine = GenesisKnowledgeEngine()
