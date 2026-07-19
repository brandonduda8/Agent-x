import uuid
import time


class RevenueLedger:

    def __init__(self):
        self.revenue = []


    def record(self, deal):

        entry = {
            "id": f"revenue_{uuid.uuid4().hex[:8]}",
            "company": deal["company"],
            "amount": deal["value"],
            "timestamp": time.time()
        }

        self.revenue.append(entry)

        print(
            f"💵 Revenue recorded: ${deal['value']}"
        )

        return entry


revenue_ledger = RevenueLedger()
