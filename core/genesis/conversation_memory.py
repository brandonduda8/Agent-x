import time
import json
import os


class GenesisConversationMemory:

    def __init__(self):

        self.system = "GENESIS CONVERSATION MEMORY v1"

        self.file = "workspace/genesis_conversations.json"

        self.messages = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            with open(self.file,"r") as f:
                self.messages = json.load(f)



    def save(self):

        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )

        with open(self.file,"w") as f:

            json.dump(
                self.messages,
                f,
                indent=2
            )



    def remember(
        self,
        source,
        message,
        response=None
    ):

        record = {

            "source": source,

            "message": message,

            "response": response,

            "timestamp": time.time()

        }


        self.messages.append(record)

        self.save()

        return record



    def recent(self, limit=10):

        return self.messages[-limit:]



    def report(self):

        return {

            "system": self.system,

            "conversations": len(self.messages),

            "timestamp": time.time()

        }


conversation_memory = GenesisConversationMemory()
