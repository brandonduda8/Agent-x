import time
import uuid
import json
import os


class GenesisLeadIntelligenceFabric:
    """
    GENESIS LEAD INTELLIGENCE FABRIC v1

    Converts discovered leads into:
    - enriched prospect intelligence
    - opportunity scoring
    - sales-ready records
    - persistent revenue memory
    """

    def __init__(self):
        self.system = "GENESIS LEAD INTELLIGENCE FABRIC v1"
        self.file = "data/genesis_lead_intelligence.json"
        self.leads = []

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    data = json.load(f)

                self.leads = data.get("leads", [])

            except Exception:
                self.leads = []

        else:
            self.save()


    def save(self):
        with open(self.file, "w") as f:
            json.dump(
                {
                    "system": self.system,
                    "leads": self.leads,
                    "updated": time.time()
                },
                f,
                indent=2
            )


    def analyze_problem(self, problem):
        problem = problem.lower()

        signals = []

        if "manual" in problem:
            signals.append("workflow_automation")

        if "slow" in problem:
            signals.append("customer_response")

        if "missed" in problem:
            signals.append("appointment_recovery")

        if not signals:
            signals.append("business_process_improvement")

        return signals


    def calculate_score(self, lead):

        score = 50

        if lead.get("opportunity"):
            score += 20

        if lead.get("problem"):
            score += 20

        if lead.get("contact") != "unknown":
            score += 10

        return min(score,100)


    def enrich_lead(self, lead):

        intelligence = {
            "id":
                "intelligence_" + uuid.uuid4().hex[:8],

            "company":
                lead.get("company"),

            "original_problem":
                lead.get("problem"),

            "automation_opportunities":
                self.analyze_problem(
                    lead.get("problem","")
                ),

            "recommended_offer":
                "AI Automation Growth System",

            "automation_score":
                0,

            "status":
                "QUALIFIED",

            "created":
                time.time()
        }


        intelligence["automation_score"] = (
            self.calculate_score(intelligence)
        )


        self.leads.append(intelligence)

        self.save()


        print(
            "🧠 Lead Intelligence Created:",
            intelligence["company"],
            "Score:",
            intelligence["automation_score"]
        )


        return intelligence



    def analyze_campaign(self, campaign):

        results = []

        for item in campaign:

            lead = item.get("lead",{})

            results.append(
                self.enrich_lead(lead)
            )

        return results



    def report(self):

        return {
            "system": self.system,
            "qualified_leads": len(self.leads),
            "status": "ONLINE",
            "timestamp": time.time()
        }



genesis_lead_intelligence_fabric = (
    GenesisLeadIntelligenceFabric()
)
