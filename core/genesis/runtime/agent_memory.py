import time
import uuid


class GenesisAgentMemory:

    def __init__(self):
        self.system = "GENESIS AGENT MEMORY v1"
        self.memories = []


    def store(self, agent, event, data):

        print(f"🧠 Memory stored for {agent}")

        memory = {
            "id": "agent_memory_" + uuid.uuid4().hex[:8],
            "agent": agent,
            "event": event,
            "data": data,
            "timestamp": time.time()
        }

        self.memories.append(memory)

        return memory


    def recall(self, agent):

        return [
            memory
            for memory in self.memories
            if memory["agent"] == agent
        ]


    def report(self):

        return {
            "system": self.system,
            "memories": len(self.memories),
            "timestamp": time.time()
        }


agent_memory = GenesisAgentMemory()
