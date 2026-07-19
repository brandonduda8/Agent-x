import time
import uuid


class ConversationMemory:

    def __init__(self):
        self.conversations = []


    def store(self, company, message, result):

        memory = {
            "id": f"conversation_{uuid.uuid4().hex[:8]}",
            "company": company,
            "message": message,
            "result": result,
            "timestamp": time.time()
        }

        self.conversations.append(memory)

        print("🧠 Conversation memory stored")

        return memory


conversation_memory = ConversationMemory()
