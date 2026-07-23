import time


class GenesisLeadQualificationEngine:

    def __init__(self):
        self.system = "GENESIS LEAD QUALIFICATION ENGINE v1"

    def qualify(self, opportunities):

        qualified = []

        for item in opportunities:

            score = 0

            category = item.get("category", "")

            if category == "Employment":
                score += 5

            if category == "Contract Work":
                score += 5

            if category == "AI Services":
                score += 4

            if category == "Stability Resources":
                score += 5

            qualified.append({
                "category": category,
                "goal": item.get("goal"),
                "qualification_score": score,
                "status": "QUALIFIED",
                "next_action": "CREATE_OUTREACH"
            })

        qualified.sort(
            key=lambda x: x["qualification_score"],
            reverse=True
        )

        return {
            "system": self.system,
            "status": "ONLINE",
            "qualified_opportunities": qualified,
            "timestamp": time.time()
        }


genesis_lead_qualification_engine = GenesisLeadQualificationEngine()
