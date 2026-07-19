import uuid
import time


class ProposalGenerator:

    def create(self, company, value):

        proposal = {
            "id": f"proposal_{uuid.uuid4().hex[:8]}",
            "company": company,
            "offer": "AI Automation Implementation Package",
            "value": value,
            "status": "READY",
            "timestamp": time.time()
        }

        print("📄 Proposal generated")

        return proposal


proposal_generator = ProposalGenerator()
