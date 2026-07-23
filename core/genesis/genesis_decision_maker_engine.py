import time
import uuid
import json
import os


class GenesisDecisionMakerEngine:

    def __init__(self):

        self.system = "GENESIS DECISION MAKER DISCOVERY ENGINE v1"
        self.file = "data/genesis_decision_makers.json"
        self.targets = []

        os.makedirs("data", exist_ok=True)

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:
                    self.targets = json.load(f).get(
                        "decision_makers",
                        []
                    )

            except:

                self.targets = []


    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                {
                    "system": self.system,
                    "decision_makers": self.targets,
                    "updated": time.time()
                },
                f,
                indent=2
            )


    def discover(self, company):

        name = company.get(
            "company",
            "UNKNOWN"
        )


        target = {

            "id":
                "decision_"
                + uuid.uuid4().hex[:8],

            "company":
                name,

            "industry":
                company.get(
                    "industry",
                    "Unknown"
                ),

            "decision_roles":[

                "Founder",

                "Owner",

                "CEO",

                "Managing Partner",

                "Operations Manager"

            ],

            "primary_contact_role":
                "Owner / CEO",

            "buying_authority_score":
                80,

            "pain_alignment":[

                "slow lead response",

                "manual follow ups",

                "lost opportunities",

                "workflow inefficiency"

            ],

            "recommended_offer":
                "AI Automation Growth System",

            "next_action":
                "PERSONALIZED_OUTREACH",

            "status":
                "READY_FOR_CONTACT",

            "created":
                time.time()

        }


        self.targets.append(target)

        self.save()


        print(
            f"👤 Decision Maker Profile Created: {name}"
        )


        return target



    def report(self):

        return {

            "system":
                self.system,

            "decision_makers":
                len(self.targets),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_decision_maker_engine = (
    GenesisDecisionMakerEngine()
)
