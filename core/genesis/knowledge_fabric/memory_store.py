import uuid
import time


class MemoryStore:

    def __init__(self):
        self.memories = []


    def store(self, source, lesson, data=None):

        memory = {
            "id": f"memory_{uuid.uuid4().hex[:8]}",
            "source": source,
            "lesson": lesson,
            "data": data or {},
            "timestamp": time.time()
        }

        self.memories.append(memory)

        print(
            "🧠 Memory stored"
        )

        return memory


memory_store = MemoryStore()
