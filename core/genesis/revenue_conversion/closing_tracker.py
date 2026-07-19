import uuid
import time


class ClosingTracker:

    def close(self, proposal):

        deal = {
            "id": f"closed_{uuid.uuid4().hex[:8]}",
            "company": proposal["company"],
            "value": proposal["value"],
            "stage": "CUSTOMER",
            "status": "CLOSED_WON",
            "timestamp": time.time()
        }

        print("🤝 Deal closed")

        return deal


closing_tracker = ClosingTracker()
