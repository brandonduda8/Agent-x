import uuid
import time


class LearningFeedback:

    def learn(self, deal):

        lesson = {
            "id": f"lesson_{uuid.uuid4().hex[:8]}",
            "event": "CUSTOMER_ACQUIRED",
            "insight": "ROI focused automation offers convert well",
            "deal": deal["company"],
            "timestamp": time.time()
        }

        print("🧠 Sales intelligence learned")

        return lesson


learning_feedback = LearningFeedback()
