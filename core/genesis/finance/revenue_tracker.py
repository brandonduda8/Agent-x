import uuid
import time


class RevenueTracker:

    def __init__(self):
        self.records = []


    def record(self, company, amount):

        entry = {
            "id": f"revenue_{uuid.uuid4().hex[:8]}",
            "company": company,
            "amount": amount,
            "timestamp": time.time()
        }

        self.records.append(entry)

        print(f"💰 Revenue tracked: ${amount}")

        return entry


revenue_tracker = RevenueTracker()
