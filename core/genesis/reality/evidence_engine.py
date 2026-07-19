import time
import uuid


class EvidenceEngine:
    def __init__(self):
        self.artifacts = []

    def create_artifact(self, mission, data):
        artifact = {
            "id": f"artifact_{uuid.uuid4().hex[:8]}",
            "mission": mission,
            "data": data,
            "timestamp": time.time()
        }

        self.artifacts.append(artifact)

        print("🧾 Evidence artifact created")

        return artifact


evidence_engine = EvidenceEngine()
