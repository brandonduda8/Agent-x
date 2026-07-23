import os
import json
import time
import uuid


class GenesisRevenueIntelligenceEngine:
    """
    GENESIS REVENUE INTELLIGENCE ENGINE v1

    Responsibilities:
    - Store prospects
    - Score opportunities
    - Generate offers
    - Store revenue insights
    - Provide intelligence to Genesis missions
    """

    def __init__(self):

        self.system = "GENESIS REVENUE INTELLIGENCE ENGINE v1"

        self.file = "data/revenue_intelligence.json"

        os.makedirs("data", exist_ok=True)

        self.initialize()


    def initialize(self):

        if not os.path.exists(self.file):

            self.save(
                {
                    "prospects": [],
                    "offers": [],
                    "insights": []
                }
            )


    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)


    def save(self, data):

        with open(self.file, "w") as f:

            json.dump(
                data,
                f,
                indent=2
            )


    def add_prospect(
        self,
        company,
        industry,
        pain_points=None
    ):

        data = self.load()

        prospect = {

            "id":
                "prospect_" + uuid.uuid4().hex[:8],

            "company":
                company,

            "industry":
                industry,

            "pain_points":
                pain_points or [],

            "score":
                0,

            "status":
                "NEW",

            "created":
                time.time()
        }


        prospect["score"] = self.score_prospect(
            prospect
        )


        data["prospects"].append(
            prospect
        )


        self.save(data)


        print(
            f"🎯 Prospect added: {company}"
        )


        return prospect



    def score_prospect(
        self,
        prospect
    ):

        score = 0


        industry = (
            prospect.get("industry", "")
            .lower()
        )

        pain_points = (
            " ".join(
                prospect.get(
                    "pain_points",
                    []
                )
            )
            .lower()
        )


        if industry:

            score += 20


        if prospect.get("pain_points"):

            score += 30


        keywords = [

            "ai",

            "automation",

            "workflow",

            "crm",

            "sales",

            "lead",

            "customer"

        ]


        text = (
            industry
            + " "
            + pain_points
        )


        for keyword in keywords:

            if keyword in text:

                score += 10


        return min(score, 100)



    def analyze_market(self):

        data = self.load()


        for prospect in data["prospects"]:

            prospect["score"] = self.score_prospect(
                prospect
            )


        ranked = sorted(
            data["prospects"],
            key=lambda x: x["score"],
            reverse=True
        )


        insight = {

            "id":
                "insight_" + uuid.uuid4().hex[:8],

            "top_prospects":
                ranked[:5],

            "timestamp":
                time.time()
        }


        data["prospects"] = ranked

        data["insights"].append(
            insight
        )


        self.save(data)


        print(
            "🧠 Revenue intelligence analysis complete"
        )


        return insight



    def create_offer(
        self,
        niche
    ):

        offer = {

            "id":
                "offer_" + uuid.uuid4().hex[:8],

            "niche":
                niche,

            "name":
                "AI Workflow Automation Package",

            "setup_price":
                2500,

            "monthly_retainer":
                500,

            "includes":

                [

                    "AI receptionist",

                    "CRM automation",

                    "Lead follow-up system",

                    "Workflow optimization"

                ],

            "created":
                time.time()
        }


        data = self.load()


        data["offers"].append(
            offer
        )


        self.save(data)


        print(
            "💰 Revenue offer created"
        )


        return offer



    def report(self):

        data = self.load()


        return {

            "system":
                self.system,

            "prospects":
                len(
                    data["prospects"]
                ),

            "offers":
                len(
                    data["offers"]
                ),

            "insights":
                len(
                    data["insights"]
                ),

            "timestamp":
                time.time()
        }



revenue_intelligence_engine = (
    GenesisRevenueIntelligenceEngine()
)
