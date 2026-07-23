import time


class GenesisOutreachGenerator:

    def __init__(self):
        self.system = "GENESIS OUTREACH GENERATOR v1"

    def generate(self, opportunities):

        outreach = []

        for item in opportunities:

            category = item.get("category")

            if category == "Employment":
                message = (
                    "Application packet: resume update, "
                    "availability message, employer follow-up"
                )

            elif category == "Contract Work":
                message = (
                    "Client proposal packet: service offer, "
                    "value statement, discovery questions"
                )

            elif category == "AI Services":
                message = (
                    "Business outreach packet: automation audit, "
                    "AI receptionist offer, meeting request"
                )

            elif category == "Stability Resources":
                message = (
                    "Resource inquiry packet: housing options, "
                    "assistance questions, follow-up tracking"
                )

            else:
                message = "General outreach packet"

            outreach.append({
                "category": category,
                "goal": item.get("goal"),
                "outreach_package": message,
                "status": "READY_TO_SEND"
            })

        return {
            "system": self.system,
            "status": "ONLINE",
            "outreach": outreach,
            "timestamp": time.time()
        }


genesis_outreach_generator = GenesisOutreachGenerator()
