import time
import uuid


class OpportunityTracker:

    def __init__(self):
        self.opportunities = []


    def create_opportunity(self, contact, offer):

        opportunity = {
            "id": f"opportunity_{uuid.uuid4().hex[:8]}",
            "company": contact["company"],
            "offer": offer,
            "stage": "PROSPECT",
            "value": 5000,
            "created": time.time()
        }

        self.opportunities.append(opportunity)

        print("🎯 Opportunity created")

        return opportunity


opportunity_tracker = OpportunityTracker()
