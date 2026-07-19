import uuid
import time


class ProspectingAgent:

    def find_prospects(self, market):

        prospects = [
            f"{market} Company 1",
            f"{market} Company 2",
            f"{market} Company 3",
            f"{market} Company 4",
            f"{market} Company 5"
        ]

        result = {
            "id": f"prospects_{uuid.uuid4().hex[:8]}",
            "market": market,
            "prospects": prospects,
            "count": len(prospects),
            "timestamp": time.time()
        }

        print("🔎 Prospecting Agent found leads")

        return result


prospecting_agent = ProspectingAgent()
