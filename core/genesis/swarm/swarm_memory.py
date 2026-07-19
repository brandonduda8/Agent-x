import time
import uuid


class GenesisSwarmMemory:

    def __init__(self):
        self.system = "GENESIS SWARM MEMORY v1"
        self.memories = []


    def store(self, swarm, knowledge):

        memory = {
            "id": "swarm_memory_" + uuid.uuid4().hex[:8],
            "swarm": swarm,
            "knowledge": knowledge,
            "timestamp": time.time()
        }

        self.memories.append(memory)

        print("🧠 Swarm memory stored:", swarm)

        return memory


    def recall(self, swarm=None):

        if swarm:
            return [
                m for m in self.memories
                if m["swarm"] == swarm
            ]

        return self.memories


    def report(self):

        return {
            "system": self.system,
            "memories": len(self.memories),
            "timestamp": time.time()
        }


swarm_memory = GenesisSwarmMemory()
