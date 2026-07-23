import time
import json
import os
import uuid


class GenesisOutreachIntelligenceEngine:

    def __init__(self):

        self.system = "GENESIS OUTREACH INTELLIGENCE ENGINE v1"

        self.input_file = (
            "data/genesis_sales_decisions.json"
        )

        self.output_file = (
            "data/genesis_outreach_campaigns.json"
        )

        self.campaigns = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(self.output_file):

            try:

                with open(self.output_file,"r") as f:
                    data = json.load(f)

                self.campaigns = data.get(
                    "campaigns",
                    []
                )

            except Exception:

                self.campaigns = []



    def save(self):

        with open(self.output_file,"w") as f:

            json.dump(
                {
                    "system": self.system,
                    "campaigns": self.campaigns,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def load_decisions(self):

        if not os.path.exists(
            self.input_file
        ):
            return []

        with open(
            self.input_file,
            "r"
        ) as f:

            return json.load(f).get(
                "decisions",
                []
            )



    def create_campaign(self, decision):

        company = decision.get(
            "company",
            "Business"
        )

        offer = decision.get(
            "recommended_offer",
            "AI Automation System"
        )


        campaign = {

            "id":
                "campaign_"
                +
                uuid.uuid4().hex[:8],

            "company":
                company,

            "decision":
                decision.get(
                    "decision"
                ),

            "email":

                {
                    "subject":
                        f"AI automation opportunity for {company}",

                    "message":
                        f"""
Hello {company},

I noticed many businesses struggle with slow customer response and repetitive workflows.

We help companies implement {offer} to save time, improve customer experience, and capture missed opportunities.

Would you be open to a quick conversation to see if automation could help your team?

Best,
Genesis AI Automation Team
"""
                },


            "linkedin":

                f"""
Hi {company}, we help businesses automate repetitive workflows and improve customer response using AI. Would love to connect and share a few ideas.
""",


            "follow_up":

                [
                    "Follow up after 3 days with ROI example",
                    "Follow up after 7 days with case study",
                    "Follow up after 14 days with final check-in"
                ],


            "status":
                "READY_TO_SEND",

            "created":
                time.time()

        }


        return campaign



    def run(self):

        decisions = self.load_decisions()

        results = []


        for decision in decisions:

            campaign = self.create_campaign(
                decision
            )

            self.campaigns.append(
                campaign
            )

            results.append(
                campaign
            )


            print(
                "📨 Outreach Created:",
                campaign["company"]
            )


        self.save()


        return {

            "system": self.system,

            "campaigns_created":
                len(results),

            "campaigns":
                results,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()
        }



    def report(self):

        return {

            "system":
                self.system,

            "campaigns":
                len(self.campaigns),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_outreach_intelligence_engine = (
    GenesisOutreachIntelligenceEngine()
)
