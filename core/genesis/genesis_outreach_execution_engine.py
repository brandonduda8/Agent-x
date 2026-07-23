import time
import json
import os


class GenesisOutreachExecutionEngine:

    def __init__(self):
        self.file = "data/genesis_outreach_queue.json"
        self.queue = []
        self.load()


    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self.queue = json.load(f)
        except Exception:
            self.queue = []


    def save(self):
        os.makedirs("data", exist_ok=True)

        with open(self.file, "w") as f:
            json.dump(
                self.queue,
                f,
                indent=2
            )


    def create_packet(self, category, target, agent):

        packet = {
            "category": category,
            "target": target,
            "agent": agent,
            "status": "PREPARED",
            "timestamp": time.time()
        }

        self.queue.append(packet)

        self.save()

        return packet


    def status(self):

        return {
            "system": "GENESIS OUTREACH EXECUTION ENGINE v1",
            "status": "ONLINE",
            "queue": self.queue,
            "count": len(self.queue),
            "timestamp": time.time()
        }


outreach_engine = GenesisOutreachExecutionEngine()
