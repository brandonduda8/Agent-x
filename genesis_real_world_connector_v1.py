import time
import uuid


class GenesisRealWorldConnector:

    def __init__(self):
        self.opportunities = []


    def add_opportunity(self, category, source, title, details):

        opportunity = {
            "id": "opp_" + str(uuid.uuid4())[:8],
            "category": category,
            "source": source,
            "title": title,
            "details": details,
            "match_score": 0,
            "status": "DISCOVERED",
            "approval_required": True,
            "created": time.time()
        }

        self.opportunities.append(opportunity)
        return opportunity


    def score_opportunity(self, opportunity):

        score = 0
        title = opportunity["title"].lower()

        if "support" in title:
            score += 40

        if "technical" in title:
            score += 30

        if "remote" in title:
            score += 20

        if "ai" in title or "automation" in title:
            score += 25

        opportunity["match_score"] = score

        if score >= 70:
            opportunity["priority"] = "CRITICAL"
        elif score >= 40:
            opportunity["priority"] = "HIGH"
        else:
            opportunity["priority"] = "NORMAL"

        return opportunity


    def discover_seed_opportunities(self):

        seeds = [
            {
                "category": "employment",
                "source": "Job Adapter",
                "title": "Remote Technical Support Specialist",
                "details": "Customer service + technology pathway"
            },
            {
                "category": "employment",
                "source": "Job Adapter",
                "title": "Remote Customer Support Position",
                "details": "Immediate income opportunity"
            },
            {
                "category": "contract",
                "source": "Freelance Adapter",
                "title": "AI Automation Assistant Project",
                "details": "AI systems and automation work"
            },
            {
                "category": "business_leads",
                "source": "Business Adapter",
                "title": "Dental Clinic AI Receptionist Opportunity",
                "details": "Automation service prospect"
            },
            {
                "category": "housing",
                "source": "Housing Adapter",
                "title": "Rental Assistance Resource",
                "details": "Housing stability support"
            }
        ]

        results = []

        for item in seeds:
            opp = self.add_opportunity(**item)
            results.append(self.score_opportunity(opp))

        return results


    def status(self):

        return {
            "system": "GENESIS REAL-WORLD CONNECTOR v1",
            "status": "ONLINE",
            "opportunities": self.opportunities,
            "count": len(self.opportunities),
            "timestamp": time.time()
        }


real_world_connector = GenesisRealWorldConnector()
