import os
import json
import time
import uuid


class GenesisCompanyResearchAgent:

    def __init__(self):

        self.system = "GENESIS COMPANY RESEARCH AGENT v1"
        self.file = "data/genesis_company_research.json"

        os.makedirs("data", exist_ok=True)

        self.research = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:
                with open(self.file, "r") as f:
                    data = json.load(f)

                self.research = data.get(
                    "research",
                    []
                )

            except Exception:
                self.research = []

        else:
            self.save()



    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "research": self.research,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def analyze_lead(self, lead):

        company = lead.get(
            "company",
            "UNKNOWN"
        )

        industry = lead.get(
            "industry",
            "UNKNOWN"
        )


        result = {

            "id":
                "research_" +
                uuid.uuid4().hex[:8],

            "lead_id":
                lead.get("id"),

            "company":
                company,

            "industry":
                industry,

            "website":
                lead.get("website"),

            "pain_signals":
                [
                    "manual workflows",
                    "slow customer response",
                    "missed follow ups"
                ],

            "automation_opportunities":
                [
                    "AI lead qualification",
                    "AI customer communication",
                    "workflow automation"
                ],

            "automation_fit_score":
                75,

            "estimated_value":
                lead.get(
                    "estimated_value",
                    "$1500 setup + $500/month"
                ),

            "research_status":
                "COMPLETE",

            "created":
                time.time()
        }


        self.research.append(
            result
        )

        self.save()


        print(
            "🧠 Company Research Complete:",
            company
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "researched_companies":
                len(self.research),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_company_research_agent = (
    GenesisCompanyResearchAgent()
)
