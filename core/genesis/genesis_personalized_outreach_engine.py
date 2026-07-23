import time
import uuid
import json
import os


class GenesisPersonalizedOutreachEngine:

    def __init__(self):

        self.system = "GENESIS PERSONALIZED OUTREACH INTELLIGENCE ENGINE v1"
        self.file = "data/genesis_personalized_outreach.json"
        self.campaigns = []

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:
                    self.campaigns = json.load(f).get(
                        "campaigns",
                        []
                    )

            except:

                self.campaigns = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "campaigns": self.campaigns,
                    "updated": time.time()
                },
                f,
                indent=2
            )


    def create_campaign(self, decision):

        company = decision.get(
            "company",
            "Company"
        )

        offer = decision.get(
            "recommended_offer",
            "AI Automation"
        )


        campaign = {

            "id":
                "outreach_"
                + uuid.uuid4().hex[:8],

            "company":
                company,

            "target_role":
                decision.get(
                    "primary_contact_role"
                ),

            "email": {

                "subject":
                    f"AI automation opportunity for {company}",

                "message":
                    f"""
Hello {company},

I noticed many real estate companies lose opportunities because leads are not followed up with quickly enough.

We help companies implement {offer} to automate lead qualification, customer communication, and follow-up workflows.

Would you be open to a quick conversation to see if automation could help your team capture more opportunities?

Best,
Genesis AI Automation Team
"""

            },


            "linkedin":

                f"""
Hi {company}, we help real estate teams automate lead qualification and follow-up using AI.

Would love to connect and share a few ideas.
""",


            "follow_up":[

                "Day 3: Send ROI example",

                "Day 7: Share automation case study",

                "Day 14: Final follow-up"

            ],


            "status":
                "READY_TO_SEND",


            "created":
                time.time()

        }


        self.campaigns.append(
            campaign
        )

        self.save()


        print(
            f"📨 Personalized Outreach Created: {company}"
        )


        return campaign



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



genesis_personalized_outreach_engine = (
    GenesisPersonalizedOutreachEngine()
)
