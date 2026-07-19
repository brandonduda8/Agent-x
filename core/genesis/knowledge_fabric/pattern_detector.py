import uuid
import time


class PatternDetector:

    def detect(self, memories):

        patterns = []

        for memory in memories:

            patterns.append({
                "pattern":
                memory["lesson"],
                "confidence":95
            })


        result = {
            "id": f"pattern_{uuid.uuid4().hex[:8]}",
            "patterns": patterns,
            "timestamp": time.time()
        }

        print(
            "🔎 Patterns detected"
        )

        return result


pattern_detector = PatternDetector()
