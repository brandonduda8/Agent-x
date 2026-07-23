import json
import os
import time


class GenesisLeadPriorityEngine:

    def __init__(self):

        self.system = (
            "GENESIS LEAD PRIORITY ENGINE v1"
        )

        self.input_file = (
            "data/genesis_lead_intelligence.json"
        )

        self.output_file = (
            "data/genesis_priority_queue.json"
        )


    def load_leads(self):

        if not os.path.exists(self.input_file):
            return []

        with open(self.input_file, "r") as f:
            data = json.load(f)

        return data.get(
            "leads",
            []
        )


    def score_lead(self, lead):

        automation = lead.get(
            "automation_score",
            0
        )

        opportunity = len(
            lead.get(
                "automation_opportunities",
                []
            )
        ) * 10


        pain_score = 50

        offer_fit = 70


        priority = int(
            (
                automation +
                opportunity +
                pain_score +
                offer_fit
            )
            / 4
        )


        return {

            **lead,

            "pain_score":
                pain_score,

            "offer_fit":
                offer_fit,

            "priority_score":
                priority,

            "recommended_action":
                (
                    "CONTACT_FIRST"
                    if priority >= 70
                    else
                    "NURTURE"
                ),

            "analyzed":
                time.time()
        }



    def build_queue(self):

        leads = self.load_leads()

        ranked = []


        for lead in leads:

            ranked.append(
                self.score_lead(
                    lead
                )
            )


        ranked.sort(
            key=lambda x:
                x["priority_score"],
            reverse=True
        )


        with open(
            self.output_file,
            "w"
        ) as f:

            json.dump(
                {
                    "system":
                        self.system,

                    "priority_queue":
                        ranked,

                    "updated":
                        time.time()
                },
                f,
                indent=2
            )


        return ranked



    def report(self):

        queue = self.build_queue()

        return {

            "system":
                self.system,

            "ranked_leads":
                len(queue),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_lead_priority_engine = (
    GenesisLeadPriorityEngine()
)
