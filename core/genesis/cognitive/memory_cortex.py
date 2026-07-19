import time
import uuid


class GenesisMemoryCortex:

    def __init__(self):
        self.system = "GENESIS MEMORY CORTEX v1"
        self.memories = []

    def store(self, event_type, data):

        memory = {
            "id": "memory_" + uuid.uuid4().hex[:8],
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        }

        self.memories.append(memory)

        print("🧠 Memory stored:", event_type)

        return memory


    def recall(self, event_type=None):

        if event_type:
            return [
                m for m in self.memories
                if m["type"] == event_type
            ]

        return self.memories


    def report(self):

        return {
            "system": self.system,
            "memories": len(self.memories),
            "timestamp": time.time()
        }


memory_cortex = GenesisMemoryCortex()
